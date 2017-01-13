```bash
conda create -n mpworks python=2.7 anaconda
pip install boltons tqdm fireworks
# set up hostname for Mendel in ~/.ssh/config
ssh -l <username> -L57003:mongodb03.nersc.gov:27017 -L57001:mongodb01.nersc.gov:27017 -L57004:mongodb04.nersc.gov:27017 <nersc/mendel-hostname> '/bin/bash -c "while [[ 1 ]]; do echo heartbeat; sleep 300; done"'
# save db credentials in my_launchpad.yaml and my_fworker.yaml
```
