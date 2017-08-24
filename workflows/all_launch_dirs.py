import json, os, tarfile, sys
from multiprocessing import Process, current_process
from datetime import date

nproc = 10
directories = [
    '/project/projectdirs/matgen/garden',
    '/project/projectdirs/matgen/scratch'
]

with open('launch_dirs.json', 'r') as f:
  log = json.load(f)
  print('# launch dirs:\t', len(log['launch_dirs']))

for i in range(nproc):
  fn = 'launch_dirs_worker{}.json'.format(i)
  if os.path.exists(fn):
    with open(fn, 'r') as f:
      d = json.load(f)
      log['parsed'] += d['parsed']
      log['launch_dirs'].update(d['launch_dirs'])

with open('launch_dirs.json', 'w') as f:
  json.dump(log, f)
  nr_launch_dirs_last_saved = len(log['launch_dirs'])

out = os.path.join('old_output', str(date.today()))
if not os.path.exists(out):
  os.mkdir(out)

for i in range(nproc):
  fn = 'launch_dirs_worker{}.json'.format(i)
  if os.path.exists(fn):
    os.rename(fn, os.path.join(out, fn))

print('# launch dirs:\t', nr_launch_dirs_last_saved)
print('# parsed:\t', len(log['parsed']))

#sys.exit(0)

def is_vasp_filename(f):
  return bool('INCAR' in f or 'OUTCAR' in f or 'vasprun.xml' in f)

def func(tarblocks, d):
  name = current_process().name
  print(name, 'starting')
  with open('launch_dirs.json.empty', 'r') as f:
    local_log = json.load(f)
  for tarblock in tarblocks:
    tarpath = os.path.join(d, tarblock)
    print(name, 'tarpath =', tarpath)
    tar = tarfile.open(tarpath, "r:gz")
    for f in tar.getnames():
      if is_vasp_filename(f):
        path = os.path.dirname(f).split(os.sep)
        idx = -1
        if 'relax' in path[idx]:
          idx -= 1
        launch_dir = os.sep.join([d] + path[:idx] + [path[idx]])
        local_log['launch_dirs'][path[idx]] = launch_dir
    print(name, 'saving', tarblock)
    local_log['parsed'].append(tarblock)
    with open('launch_dirs_{}.json'.format(name), 'w') as f:
      json.dump(local_log, f)

try:

  curdir = None
  for directory in directories:
    print(directory.upper())
    for root, dirs, files in os.walk(directory):
      if root == directory:
        tarblocks = [f for f in files if '.tar.gz' in f and f not in log['parsed']]
        print('{} tarred blocks'.format(len(tarblocks)))
        jobs = []
        n = int(len(tarblocks)/nproc)+1
        chunks = [tarblocks[i:i + n] for i in range(0, len(tarblocks), n)]
        for i in range(nproc):
          p = Process(name='worker{}'.format(i), target=func, args=(chunks[i], directory))
          jobs.append(p)
          p.start()
      else:
        path = root.split(os.sep)
        checkpoint = bool(len(path) == 6)
        if checkpoint:
          if curdir is not None:
              log['parsed'].append(curdir)
          curdir = os.path.basename(root)
          if curdir in log['parsed']:
            dirs[:] = [] # stop decending
          nr_launch_dirs = len(log['launch_dirs'])
          print('checkpoint', curdir, nr_launch_dirs, len(dirs))
          if nr_launch_dirs - nr_launch_dirs_last_saved > 5000:
            with open('launch_dirs.json', 'w') as f:
              json.dump(log, f)
              nr_launch_dirs_last_saved = len(log['launch_dirs'])
            print('saved launch dirs')
        else:
          if path[-1] in log['launch_dirs']:
            continue
          for f in files:
            if is_vasp_filename(f):
              log['launch_dirs'][path[-1]] = root
              break

except:
  with open('launch_dirs.json', 'w') as f:
      json.dump(log, f)
  print('# of launch dirs:', len(log['launch_dirs']))
  raise

with open('launch_dirs.json', 'w') as f:
    json.dump(log, f)
print('# of launch dirs:', len(log['launch_dirs']))
