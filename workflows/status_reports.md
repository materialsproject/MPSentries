### 2017-02-01

- 66/77 COMPLETED Kitchaev Workflows; 2 RUNNING
- Mark McAdon (DOW): Re2O7, 1370872 RUNNING
- George Yumnam: 1566138 FIZZLED (also 1566120, 1566104, 1566099, 1567504, 1567491) -> RE-RUNNING
  * 1566099 FIZZLED
- http://fireworks.dash.materialsproject.org/?fw_query=&wf_query=%7B%22nodes%22%3A%7B%22%24in%22%3A%5B1370872%2C1566138%2C1566120%2C+1566104%2C+1566099%2C+1567504%2C+1567491%2C1563287%2C+1652717%5D%7D%7D


### 2017-01-31

65/77 COMPLETED Kitchaev Workflows; 1652735 PAUSED (see 2017-01-30)

### 2017-01-30

#### Kitchaev Workflows

- 63/77 COMPLETED Kitchaev Workflows
- 10 FIZZLED
  * VASP db insertion [1563973, 1563457, 1563651]: "successful, but don't know how to continue"
  * GGA+U optimize structure (2x) [1563253, 1563247]: MaxErrors
  * GGA+U static v2 [1563654]: PositiveEnergyErrorHandler
  * GGA optimize structure (2x) [1563137, 1562957]: FrozenJobErrorHandler / VaspRunXMLValidator
  * GGA+U band structure v2 [1564136]: VaspRunXMLValidator
  * Controller: add Electronic Structure v2 [1563363]: "KeyError: 'analysis'"
- re-running the FIZZLED GGA fireworks on Mendel
- 1 RUNNING [1563287] for more than 2 days -> increased walltime
- 3 PAUSED [1652670, 1652672, 1652674] keep generating dynamic fireworks due to un-converged SO calculation


### 2017-01-27

- 62/77 COMPLETED Kitchaev workflows
- 3 workflows (1652670, 1652672, 1652674) keep generating dynamic fireworks
  due to un-converged SO calculation -> PAUSED

### 2017-01-26

- 54/77 COMPLETED Kitchaev workflows

### 2017-01-25

- 1 READY user-submitted Add-to-SNL task -> COMPLETED
- 50/77 COMPLETED Kitchaev workflows

### 2017-01-24

#### incomplete user-submitted "Add to SNL tasks"

- unlock and rerun 91 tasks (excl. ICSD, Pauling File, and Heusler submissions) 
  -> permanently include in query to get duplicate checking done during debugging
- no tasks in states other than READY
- All 91 tasks COMPLETED

####  Piezoelectricity Workflows

all workflows COMPLETED:  
http://fireworks.dash.materialsproject.org/?fw_query=&wf_query=%7B%22metadata.submission_group_id%22%3A+118151%7D

#### Kitchaev Workflows

49/77 COMPLETED

### 2017-01-23

- 48 COMPLETED Kitchaev workflows, others ~70% done
- Piezeoelectric 50-70% done

### 2017-01-20

- start remaining 4 READY workflows for Piezoelectricity (see 2017-01-19)
- continue 24 RUNNING workflows for Kitchaev (43 COMPLETED, 10 FIZZLED)

### 2017-01-19

#### user-submitted Workflows

4017 RUNNING workflows (13.2%)  
4850 FIZZLED workflows (16.0%)  
19000 READY workflows (62.6%)  
2434 COMPLETED workflows (8.0%)  
44 DEFUSED workflows (0.1%)  
=> 30345 workflows in total

#### Kitchaev Workflows

- 41/77 COMPLETED (24 RUNNING, 12 FIZZLED)
- `lpad reignite_fws -i 1563363` (was defused, reason unknown)
- `lpad admin unlock -i 1563108 1563186 1563158` (fizzled due to locked DB)
- `lpad rerun_fws -i 1563108, 1563186, 1563158` -> all completed
- fizzled workflow 1563973 (possibly same for 1563457, 1563651):

    ```
    1563972 contains relax1 and relax2 which are unconverged VASP runs with
    Electronic convergence reached: True.
    Ionic convergence reached: False.
    ```

####  Piezoelectricity Workflows

- remark: {Ti,Zr,Hf}-Zn-N piezoelectricity study
- 11/15 COMPLETED (4 READY)
- READY: 1583655, 1583643, 1583631, 1583607

#### Heusler Phases Workflows

- remark: Heusler ABC2 phases
- 5/2371 COMPLETED (1576 FIZZLED)

#### ICSD 2015 Workflows

- remark: new ICSD batch
- 800/1908 COMPLETED (558 FIZZLED)

#### Pauling File Workflows

- remark: Pauling file
- 26/23370 COMPLETED (18k READY)

### 2017-01-10

- 30241 user-submitted workflows
- 4853 fizzled workflows (16.0%)
- 702 / 4853 workflows have duplicate launch_dirs => 4151 unique launch_dirs
- 3981      launchdirs_exist.txt  
  170      launchdirs_not_exist.txt
- Errors:  

  ```
  1049      AttributeError -- 'NoneType' object has no attribute 'group' -- inputs.py#1411
  804      local_dir not found
  762      error file not found in local_dir
  383      RuntimeError -- (CustodianError(...), u'Unrecoverable erro -- custodian.py#221
  308      other
  185      ValueError -- DB insertion successful, but don't know how to               -- vasp_io_tasks.py#241
  170      remote_dir not found
  153      ValueError -- Could not lock DB even after 5.0 minutes! -- snl_mongo.py#183
  80      RuntimeError -- (CustodianError(...), u'Validation failed: -- custodian.py#221
  57      ValueError -- DB insertion successful, but don't know how to               -- vasp_io_tasks.py#240
  3951
  ```

#### Kitchaev Workflows:

  ```
  3      1563651      ValueError -- DB insertion successful, but don't know how to     -- vasp_io_tasks.py#240
  3      1563108      ValueError -- Could not lock DB even after 5.0 minutes! -- snl_mongo.py#183
  2      1563137      RuntimeError -- (CustodianError(...), u'Unrecove -- custodian.py#221
  2      1563247      RuntimeError -- (CustodianError(...), u'MaxError -- custodian.py#221
  2      1564136      RuntimeError -- (CustodianError(...), u'Validati -- custodian.py#221
  1      1564191      no errors parsed
  13
  ```
