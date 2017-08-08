#!/usr/bin/env python

import json, time
from pymongo import MongoClient
from fireworks.core.launchpad import LaunchPad
from gridfs import GridFS
from tqdm import tqdm

def variable_exists(var):
    return var in locals() or var in globals()
    
if not variable_exists('lpad'):
    lpad = LaunchPad.from_file('my_launchpad.yaml')

if not variable_exists('db_vasp'):
    vasp_config = json.load(open('tasks_db.json'))
    vasp_conn = MongoClient(vasp_config['host'], vasp_config['port'], j=False)
    db_vasp = vasp_conn[vasp_config['database']]
    db_vasp.authenticate(vasp_config['readonly_user'], vasp_config['readonly_password'])

if not variable_exists('fs'):
    fs = GridFS(db_vasp, 'band_structure_fs')

print('{} tasks'.format(db_vasp.tasks.count()))

UNIFORM_TYPES = ["GGA Uniform", "GGA+U Uniform", "GGA Uniform v2", "GGA+U Uniform v2"]
uniform_query = {"state": "successful", "is_compatible": True, "task_type": {"$in": UNIFORM_TYPES}}
uniform_tasks = db_vasp.tasks.find(uniform_query)
nr_uniform_tasks = uniform_tasks.count()
print('{} uniform tasks left to check for projections'.format(nr_uniform_tasks))

with open('task_fw_ids_wBS.json', 'r') as f:
    task_fw_ids_wBS = json.loads(f.read())
print('{} tasks already checked for projections'.format(len(task_fw_ids_wBS)))

with open('task_fw_ids_woBS.json', 'r') as f:
    task_fw_ids_woBS = json.loads(f.read())
print('{} tasks do not have projections'.format(len(task_fw_ids_woBS)))

ignore_tasks = task_fw_ids_wBS.keys() + task_fw_ids_woBS.keys() # remove woBS to start new scan
nr_tasks_processed = 0

for task in tqdm(uniform_tasks, total=nr_uniform_tasks):
    if task['task_id'] in ignore_tasks:
        continue
    bs_id = task['calculations'][0]['band_structure_fs_id']
    bs_dict = json.loads(fs.get(bs_id).read())
    if not bs_dict['projections']: # projections missing
        task_fw_ids_woBS[task['task_id']] = task['fw_id']
	if not nr_tasks_processed%1000:
	    with open('task_fw_ids_woBS.json', 'w') as f:
		print('{} tasks do not have projections'.format(len(task_fw_ids_woBS)))
		json.dump(task_fw_ids_woBS, f)
    else:
        task_fw_ids_wBS[task['task_id']] = task['fw_id']
	if not nr_tasks_processed%1000:
	    with open('task_fw_ids_wBS.json', 'w') as f:
		print('{} tasks already have projections'.format(len(task_fw_ids_wBS)))
		json.dump(task_fw_ids_wBS, f)
    nr_tasks_processed += 1

with open('task_fw_ids_wBS.json', 'w') as f:
    print('{} tasks already have projections'.format(len(task_fw_ids_wBS)))
    json.dump(task_fw_ids_wBS, f)

with open('task_fw_ids_woBS.json', 'w') as f:
    print('{} tasks do not have projections'.format(len(task_fw_ids_woBS)))
    json.dump(task_fw_ids_woBS, f)
