import json, os, tarfile
from collections import OrderedDict

with open('snl_tasks_atomate.json', 'r') as f:
  data = json.load(f)
  data = OrderedDict((key, data[key]) for key in sorted(data.keys()))

check_good_mpids = [
    mpid for mpid, d in data.items()
    if 'error' not in d and (
      'all_tasks_found' not in d or not d['all_tasks_found']
    )
]
print(len(check_good_mpids), 'mpids to check ...')

unpack = OrderedDict()
for idx,mpid in enumerate(check_good_mpids):
  if idx and not idx%5000:
    print(idx, '...')
  if not 'exceptions' in data[mpid]:
    tasks = data[mpid]['tasks']
    for idx, (task_id, launch_dir) in enumerate(tasks.items()):
      if not os.path.exists(launch_dir):
        tar_dir, block_idx = [], None
        launch_dir_split = launch_dir.split(os.sep)
        for ix, x in enumerate(launch_dir_split):
          tar_dir.append(x)
          if x.startswith('block_'):
            block_idx = ix
            break
        tarfile_path = os.sep.join(tar_dir) + '.tar.gz'
        if not os.path.exists(tarfile_path):
          print(mpid, task_id, 'missing tarfile_path:', tarfile_path)
          continue
        subdir = os.sep.join(launch_dir_split[block_idx:])
        if tarfile_path not in unpack:
          unpack[tarfile_path] = [subdir]
        else:
          unpack[tarfile_path].append(subdir)

print(sum([len(v) for v in unpack.values()]), 'launch_dirs to unpack')

def get_subdir_and_files(members, subdirs):
  for tarinfo in members:
    for subdir in subdirs:
      if tarinfo.name.startswith(subdir):
        yield tarinfo

for tarfile_path, subdirs in unpack.items():
  with tarfile.open(tarfile_path, "r|gz") as tar:
    print(tarfile_path)
    print('extracting', len(subdirs), 'subdirs ...')
    tar.extractall(
        path='/global/projecta/projectdirs/matgen/garden/',
        members=get_subdir_and_files(tar, subdirs)
    )
    print('DONE')
