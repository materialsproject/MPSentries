import json, yaml, os, sys
from pymongo import MongoClient
from atomate.vasp.drones import VaspDrone
from atomate.vasp.database import VaspCalcDb
from collections import OrderedDict
from multiprocessing import Process, current_process
from itertools import repeat
from tqdm import tqdm
from collections import Counter
from datetime import date

PARSE_TASKS = False
RESET = False
GARDEN = '/global/projecta/projectdirs/matgen/garden/'
nr_good_mpids, nr_bad_mpids = 30000, 50
nproc = 10

snl_db_config_path = os.path.join('snl_db.yaml')
snl_db_config_file = open(snl_db_config_path, 'r')
snl_db_config = yaml.load(snl_db_config_file)
snl_db_conn = MongoClient(snl_db_config['host'], snl_db_config['port'], j=False, connect=False)
snl_db = snl_db_conn[snl_db_config['db']]
snl_db.authenticate(snl_db_config['username'], snl_db_config['password'])
print('# of SNLs:', snl_db.snl.count())

materials_prod_config_path = os.path.join('materials_db_prod.yaml')
materials_prod_config_file = open(materials_prod_config_path, 'r')
config = yaml.load(materials_prod_config_file)
conn = MongoClient(config['host'], config['port'], j=False, connect=False)
db_jp = conn[config['db']]
db_jp.authenticate(config['user_name'], config['password'])
print('# of materials:', db_jp.materials.count())

vasp_config = json.load(open('tasks_db.json'))
vasp_conn = MongoClient(vasp_config['host'], vasp_config['port'], j=False, connect=False)
db_vasp = vasp_conn[vasp_config['database']]
db_vasp.authenticate(vasp_config['readonly_user'], vasp_config['readonly_password'])
print('# of MP tasks', db_vasp.tasks.count())

with open('snl_tasks_atomate.json', 'r') as f:
  data = json.load(f)
  data = OrderedDict((key, data[key]) for key in sorted(data.keys()))
 
if PARSE_TASKS:

  query = {} #if not data else {'task_id': {'$nin': data.keys()}}
  has_bs_piezo_dos = {'has_bandstructure': True, 'piezo': {'$exists': 1}, 'dos': {'$exists': 1}}
  #query.update(has_bs_piezo_dos)
  has_bs_dos = {'has_bandstructure': True, 'dos': {'$exists': 1}}
  query.update(has_bs_dos)
  docs = db_jp.materials.find(query, {'task_ids': 1, '_id': 0, 'task_id': 1, 'snl.snl_id': 1})

  for idx,doc in tqdm(enumerate(docs), total=docs.count()):
      mpid = doc['task_id']
      if mpid in data:
        continue
      data[mpid] = {'tasks': {}}
      if set(has_bs_piezo_dos.keys()).issubset(query.keys()):
          data[mpid]['tags'] = ['has_bs_piezo_dos']
      if set(has_bs_dos.keys()).issubset(query.keys()):
          data[mpid]['tags'] = ['has_bs_dos']
      for task_id in doc['task_ids']:
          tasks = list(db_vasp.tasks.find({'task_id': task_id}, {'dir_name': 1, '_id': 0}))
          if len(tasks) > 1:
              data[mpid]['error'] = 'found {} tasks'.format(len(tasks))
              continue
          elif not tasks:
              data[mpid]['error'] = 'no task found'
              continue
          dir_name = tasks[0]['dir_name']
          launch_dir = os.path.join(GARDEN, dir_name)
          if not os.path.exists(launch_dir):
              data[mpid]['error'] = '{} not found'.format(dir_name)
              break
          data[mpid]['tasks'][task_id] = launch_dir
      data[mpid]['snl_id'] = doc['snl']['snl_id']
      if not idx%500:
          with open('snl_tasks_atomate.json', 'w') as f:
              json.dump(data, f)
        
else:

  for i in range(nproc):
    fn = 'snl_tasks_atomate_worker{}.json'.format(i)
    if os.path.exists(fn):
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

  print('# of mp-ids:', len(data))

  #for mpid in data:
  #  if 'exceptions' in data[mpid]:
  #    for task_id, ex in data[mpid]['exceptions'].iteritems():
  #      print(mpid, task_id, ex)
  #    #data[mpid].pop('exceptions')
    
  good_mpids = [mpid for mpid, d in data.items() if 'error' not in d and 'tags' in d]
  bad_mpids = [mpid for mpid, d in data.items() if 'error' in d]
  print('total # of good mp-ids:', len(good_mpids))
  print('total # of bad mp-ids:', len(bad_mpids))

  counter = Counter()
  nr_exception_mpids = 0
  for mpid, d in data.items():
    if mpid not in good_mpids:
      continue
    if 'exceptions' in d:
      nr_exception_mpids += 1
      for task_id, exception in d['exceptions'].items():
        counter[exception[:20]] += 1
  print('# of mp-ids with exceptions:', nr_exception_mpids, 'out of', len(good_mpids))
  print(counter)

  nr_all_mpids = nr_good_mpids + nr_bad_mpids
  good_snl_ids = [data[mpid]['snl_id'] for mpid in good_mpids[:nr_good_mpids]] # all with output dir
  bad_snl_ids = [data[mpid]['snl_id'] for mpid in bad_mpids[:nr_bad_mpids]] # all without output dir
  all_snl_ids = good_snl_ids + bad_snl_ids

  db_config_atomate = json.load(open('db_atomate.json'))
  db_conn_atomate = MongoClient(db_config_atomate['host'], db_config_atomate['port'], j=False, connect=False)
  db_atomate = db_conn_atomate[db_config_atomate['database']]
  db_atomate.authenticate(db_config_atomate['admin_user'], db_config_atomate['admin_password'])
  print('# of atomate tasks:', db_atomate.tasks.count())

  if db_atomate.snls.count() == 0:
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
          break
    with open('snl_tasks_atomate_{}.json'.format(name), 'w') as f:
      json.dump(d, f)
    print(name, 'processed', len(mpids), 'mpids')

  print('check already existing tasks ...')
  drone = VaspDrone(parse_dos=True)
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
