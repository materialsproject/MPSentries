import json, yaml, os, sys
from pymongo import MongoClient
from atomate.vasp.drones import VaspDrone
from atomate.vasp.database import VaspCalcDb
from collections import OrderedDict
from multiprocessing import Process, current_process
from itertools import repeat
from collections import Counter
from datetime import date

PARSE_TASKS = False
RESET = False
ADD_SNLS = False

GARDEN = '/global/projecta/projectdirs/matgen/garden/'
nr_good_mpids, nr_bad_mpids = 40000, 50
nproc = 10

with open('snl_tasks_atomate.json', 'r') as f:
  data = json.load(f)
  data = OrderedDict((key, data[key]) for key in sorted(data.keys()))
 
merge_files = False
for i in range(nproc):
  fn = 'snl_tasks_atomate_worker{}.json'.format(i)
  if os.path.exists(fn):
    merge_files = True
    with open(fn, 'r') as f:
      data.update(json.load(f))

with open('snl_tasks_atomate.json', 'w') as f:
  json.dump(data, f)

out = os.path.join('old_output', str(date.today()))
if not os.path.exists(out):
  os.mkdir(out)

for i in range(nproc):
  fn = 'snl_tasks_atomate_worker{}.json'.format(i)
  if os.path.exists(fn):
    os.rename(fn, os.path.join(out, fn))

print('# mp-ids:\t', len(data))

good_mpids = [mpid for mpid, d in data.items() if 'error' not in d]
print('# good mp-ids:\t', len(good_mpids))
bad_mpids = [mpid for mpid, d in data.items() if 'error' in d]
print('# bad mp-ids:\t', len(bad_mpids))

counter_except = Counter()
counter_error = Counter()
nr_exception_mpids = 0

for mpid, d in data.items():
  if 'error' in d:
      if 'skipped' in d['error']:
          counter_error['skipped'] += 1
      elif 'not found' in d['error']:
          counter_error['not found'] += 1
      elif 'no task found' in d['error']:
          counter_error['no task found'] += 1
      else:
          raise ValueError(d['error'])
  elif 'exceptions' in d:
      nr_exception_mpids += 1
      for task_id, exception in d['exceptions'].items():
        counter_except[exception[:20]] += 1

print(counter_error)
print('# mp-ids w/ exceptions:', nr_exception_mpids)
print(counter_except.most_common(2))

if merge_files:
  sys.exit(0)

if PARSE_TASKS:

  materials_prod_config_path = os.path.join('materials_db_prod.yaml')
  materials_prod_config_file = open(materials_prod_config_path, 'r')
  config = yaml.load(materials_prod_config_file)
  conn = MongoClient(config['host'], config['port'], j=False, connect=False)
  db_jp = conn[config['db']]
  db_jp.authenticate(config['user_name'], config['password'])
  print('# materials:\t', db_jp.materials.count())

  with open('launch_dirs.json', 'r') as f:
    launch_dirs_log = json.load(f)

  query = {} #{'has_bandstructure': True, 'dos': {'$exists': 1}}
  mpids = db_jp.materials.find(query).distinct('task_id')
  print('PARSE - # of mpids:', len(mpids))

  vasp_config = json.load(open('tasks_db.json'))
  vasp_conn = MongoClient(vasp_config['host'], vasp_config['port'], j=False, connect=False)
  db_vasp = vasp_conn[vasp_config['database']]
  db_vasp.authenticate(vasp_config['readonly_user'], vasp_config['readonly_password'])
  print('# MP tasks:\t', db_vasp.tasks.count())

  def func(docs, d):
      name = current_process().name
      print(name, 'starting')
      for idx, doc in enumerate(docs):
          if idx and not idx%250:
              print(name, idx, 'saving ...')
              with open('snl_tasks_atomate_{}.json'.format(name), 'w') as f:
                  json.dump(d, f)
          mpid = doc['task_id']
          if mpid not in d:
              d[mpid] = {'tasks': {}}
          d[mpid]['snl_id'] = doc['snl']['snl_id']
          for task_id in doc['task_ids']:
              tasks = list(db_vasp.tasks.find({'task_id': task_id}, {'dir_name': 1, '_id': 0}))
              if len(tasks) > 1:
                  d[mpid]['error'] = '{}: found {} tasks'.format(task_id, len(tasks))
                  continue
              elif not tasks:
                  d[mpid]['error'] = '{}: no task found'.format(task_id)
                  continue
              dir_name = tasks[0]['dir_name']
              launch_dir = os.path.join(GARDEN, dir_name)
              if not os.path.exists(launch_dir):
                  launcher = dir_name.split(os.sep)[-1]
                  if not launcher in launch_dirs_log['launch_dirs']:
                      d[mpid]['error'] = '{}: {} not found'.format(task_id, dir_name)
                      continue
                  launch_dir = launch_dirs_log['launch_dirs'][launcher]
                  if 'error' in d[mpid]:
                      d[mpid].pop('error')
              d[mpid]['tasks'][task_id] = launch_dir

      print(name, 'final saving ...')
      with open('snl_tasks_atomate_{}.json'.format(name), 'w') as f:
          json.dump(d, f)
            
  mpids = [mpid for mpid in mpids if mpid not in data or 'error' in data[mpid]] # skip error free
  print('PARSE - # of mpids:', len(mpids))
  jobs = []
  n = int(len(mpids)/nproc)+1
  chunks = [mpids[i:i + n] for i in range(0, len(mpids), n)]

  for i in range(nproc):
    d = OrderedDict((key, data[key]) for key in chunks[i] if key in data)
    docs = db_jp.materials.find(
      {'task_id': {'$in': chunks[i]}},
      {'task_ids': 1, '_id': 0, 'task_id': 1, 'snl.snl_id': 1}
    )
    p = Process(name='worker{}'.format(i), target=func, args=(docs, d))
    jobs.append(p)
    p.start()

else:

  if ADD_SNLS:
    db_config_atomate = json.load(open('db_atomate.json'))
    db_conn_atomate = MongoClient(db_config_atomate['host'], db_config_atomate['port'], j=False, connect=False)
    db_atomate = db_conn_atomate[db_config_atomate['database']]
    db_atomate.authenticate(db_config_atomate['admin_user'], db_config_atomate['admin_password'])
    print('# of atomate tasks:', db_atomate.tasks.count())
    snl_db_config_path = os.path.join('snl_db.yaml')
    snl_db_config_file = open(snl_db_config_path, 'r')
    snl_db_config = yaml.load(snl_db_config_file)
    snl_db_conn = MongoClient(snl_db_config['host'], snl_db_config['port'], j=False, connect=False)
    snl_db = snl_db_conn[snl_db_config['db']]
    snl_db.authenticate(snl_db_config['username'], snl_db_config['password'])
    print('# SNLs:\t', snl_db.snl.count())
    nr_all_mpids = nr_good_mpids + nr_bad_mpids
    good_snl_ids = [data[mpid]['snl_id'] for mpid in good_mpids[:nr_good_mpids]] # all with output dir
    bad_snl_ids = [data[mpid]['snl_id'] for mpid in bad_mpids[:nr_bad_mpids]] # all without output dir
    all_snl_ids = good_snl_ids + bad_snl_ids
    all_snls = snl_db.snl.find({'snl_id': {'$in': all_snl_ids}})
    if all_snls.count() != nr_all_mpids:
      print('{} mpids but {} SNLs!'.format(nr_all_mpids, all_snls.count()))
    print(db_atomate.snls.insert_many(all_snls))

  def func(mpids, d):
    drone = VaspDrone(parse_dos=True)
    name = current_process().name
    print(name, 'starting')
    mmdb = VaspCalcDb.from_db_file('db_atomate.json', admin=True)
    for idx, mpid in enumerate(mpids):
      if idx and not idx%250:
        print(name, idx, '...')
        with open('snl_tasks_atomate_{}.json'.format(name), 'w') as f:
          json.dump(d, f)
      tasks = d[mpid]['tasks']
      for idx, (task_id, launch_dir) in enumerate(tasks.items()):
        task_doc = mmdb.collection.find_one({'task_id': task_id}, {'_id': 0, 'task_id': 1})
        if idx == 0:
          print('{} mpid = {}: {} tasks'.format(name, mpid, len(tasks)))
        if task_doc:
          continue
        print(name, 'launch_dir =',launch_dir)
        try:
          task_doc = drone.assimilate(launch_dir)
          task_doc['task_id'] = task_id
          mmdb.insert_task(task_doc, parse_dos=True, parse_bs=True)
        except Exception as ex:
          if 'exceptions' not in d[mpid]:
            d[mpid]['exceptions'] = {}
          d[mpid]['exceptions'][task_id] = str(ex)
    with open('snl_tasks_atomate_{}.json'.format(name), 'w') as f:
      json.dump(d, f)
    print(name, 'processed', len(mpids), 'mpids')

  print('check already existing tasks ...')
  drone = VaspDrone(parse_dos=True)
  if not os.path.exists('db_atomate.json'):
    print('you need credentials for the atomate task DB in db_atomate.json!')
    sys.exit(0)
  mmdb = VaspCalcDb.from_db_file('db_atomate.json', admin=True)
  if RESET:
    print('reseting mmdb ...')
    mmdb.reset()
  l = []
  for mpid in good_mpids[:nr_good_mpids]:
    tasks = data[mpid]['tasks']
    all_tasks_found = True
    for idx, (task_id, launch_dir) in enumerate(tasks.items()):
      if 'exceptions' in data[mpid] and data[mpid]['exceptions'] \
	  and not data[mpid]['exceptions'].get(task_id, '').startswith('[Errno 116]'):
        continue
      if 'exceptions' in data[mpid]:
        data[mpid].pop('exceptions') # reset for Errno 116
      task_doc = mmdb.collection.find_one({'task_id': task_id}, {'_id': 0, 'task_id': 1})
      if task_doc:
        continue
      all_tasks_found = False
      break
    if not all_tasks_found:
      l.append(mpid)

  if not l:
    print('nothing to process')
    sys.exit(0)

  print(len(l), 'mpids to process')

  jobs = []
  n = int(len(l)/nproc)+1
  chunks = [l[i:i + n] for i in range(0, len(l), n)]

  for i in range(nproc):
    d = OrderedDict((key, data[key]) for key in chunks[i])
    p = Process(name='worker{}'.format(i), target=func, args=(chunks[i], d))
    jobs.append(p)
    p.start()
