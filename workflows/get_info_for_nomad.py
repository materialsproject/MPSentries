import json, os, sys
from pymongo import MongoClient
from collections import OrderedDict, Counter

vasp_config = json.load(open('tasks_db.json'))
vasp_conn = MongoClient(vasp_config['host'], vasp_config['port'], j=False, connect=False)
db_vasp = vasp_conn[vasp_config['database']]
db_vasp.authenticate(vasp_config['readonly_user'], vasp_config['readonly_password'])
print('# MP tasks:\t', db_vasp.tasks.count())

with open('snl_tasks_atomate.json', 'r') as f:
  data = json.load(f)
  data = OrderedDict((key, data[key]) for key in sorted(data.keys()))

counter = Counter()
nomad_info = OrderedDict()

for mpid, d in data.items():
  for task_id, launch_dir in d['tasks'].items():
    for year in map(str, range(2011, 2018)):
      if year in launch_dir:
        all_tasks_found = 'all_tasks_found' in d and d['all_tasks_found']
        key = '-'.join([year, str(all_tasks_found)])
        counter[key] += 1
        if ('block_2011-' in launch_dir or 'block_2012-' in launch_dir):
            #print('block_'+launch_dir.split('block_')[-1], task_id)
            doc = db_vasp.tasks.find_one({'task_id': task_id}, {'snl.about.authors': 1})
            authors = doc['snl']['about']['authors']
            nomad_info[task_id] = {'launch_dir': launch_dir, 'authors': authors}

with open('nomad_info.json', 'w') as f:
  json.dump(nomad_info, f)

print(counter)

