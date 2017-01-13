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

 - Errors for Kitchaev Workflows:

  ```
  3      1563651      ValueError -- DB insertion successful, but don't know how to     -- vasp_io_tasks.py#240
  3      1563108      ValueError -- Could not lock DB even after 5.0 minutes! -- snl_mongo.py#183
  2      1563137      RuntimeError -- (CustodianError(...), u'Unrecove -- custodian.py#221
  2      1563247      RuntimeError -- (CustodianError(...), u'MaxError -- custodian.py#221
  2      1564136      RuntimeError -- (CustodianError(...), u'Validati -- custodian.py#221
  1      1564191      no errors parsed
  13
  ```
