### 2017-05-18

#### USC 4-layers

```
18 RUNNING workflows (2.2%)
14 FIZZLED workflows (1.7%)
405 READY workflows (48.6%)
397 COMPLETED workflows (47.6%)
834 workflows in total
```

#### Hark VW

2346 basically DONE:

```
u'COMPLETED': 2181, u'FIZZLED': 75, u'PAUSED': 40, u'DEFUSED': 23, u'WAITING': 17, u'RESERVED': 10
```


### 2017-05-15

- started running 666 USC 4-layer structures
- cleaned up Hark VW workflows and extracted meaningful statistics
- 6368 VASP db insertions out of 58459 uniform tasks rerun (for projections)

#### Hark VW

```
u'COMPLETED': 1614, u'DEFUSED': 14, u'FIZZLED': 67, u'PAUSED': 40, u'READY': 594, u'RESERVED': 5, u'WAITING': 12
```

### 2017-05-11

- all 146 3-layer USC calculations DONE
- working through VASP db insertion for projections
- defused Hark's workflows with >20 nodes to avoid endless duplicate checking
- paused all "add Electronic Structure" controllers for Hark's submissions; 1116 fireworks ready

### 2017-05-10

- ~60k VASP DB insertion tasks to rerun to save projections; 1300 done, additional 3000 queued  
  -> DONE; queued ~10k
- all USC submissions done; fixing final DB insertion for 3-layer structures  
  -> DONE; looking at remaining ~10 structures -> Add to SNL tasks fixed and rerun; all queued.
- VW Hark submissions duplicate checking?
- DOS offset fix basically all DONE
- continue new ICSD over night

#### new ICSD batch

```
341 RUNNING workflows (11.9%)
313 FIZZLED workflows (11.0%)
1970 COMPLETED workflows (69.0%)
117 RESERVED workflows (4.1%)
116 DEFUSED workflows (4.1%)
2857 workflows in total
```


### 2017-04-12

- start running non-batch submissions on XSEDE -> [LINK](http://fireworks.dash.materialsproject.org/?fw_query=%7B%22state%22%3A%22READY%22%2C%22%24and%22%3A+%5B%7B%22%24or%22%3A+%5B%7B%22spec.snl.about.remarks%22%3A+%7B%22%24in%22%3A+%5B%22MP+user+submission%22%5D%2C+%22%24nin%22%3A+%5B%22new+ICSD+batch%22%2C+%22Pauling+file%22%2C+%22Heusler+ABC2+phases%22%2C+%22proton+conducting+materials+for+fuel+cells%22%2C+%22solid+solution+metal%22%5D%7D%7D%2C+%7B%22spec.mpsnl.about.remarks%22%3A+%7B%22%24in%22%3A+%5B%22MP+user+submission%22%5D%2C+%22%24nin%22%3A+%5B%22new+ICSD+batch%22%2C+%22Pauling+file%22%2C+%22Heusler+ABC2+phases%22%2C+%22proton+conducting+materials+for+fuel+cells%22%2C+%22solid+solution+metal%22%5D%7D%7D%5D%7D%2C+%7B%22%24or%22%3A+%5B%7B%22spec.prev_vasp_dir%22%3A+%7B%22%24exists%22%3A+0%7D%7D%2C+%7B%22spec.prev_vasp_dir%22%3A+%7B%22%24regex%22%3A+%22%2Foasis%2F%22%7D%7D%5D%7D%5D%7D&wf_query=)
- NERSC [RUNNING/RESERVED/READY/WAITING]:
  * VW Hark [0/0/652/0] -> [LINK](http://fireworks.dash.materialsproject.org/?fw_query=%7B%22spec.snl.about.remarks%22%3A+%22solid+solution+metal%22%7D&wf_query=%7B%22state%22%3A+%7B%22%24ne%22%3A+%22COMPLETED%22%7D%7D)
  * ICSD Weike [23/263/18/0] -> [LINK](http://fireworks.dash.materialsproject.org/?fw_query=%7B%22%24or%22%3A+%5B%7B%22spec.snl.about.remarks%22%3A+%22new+ICSD+batch%22%7D%2C+%7B%22spec.mpsnl.about.remarks%22%3A+%22new+ICSD+batch%22%7D%5D%7D&wf_query=%7B%22state%22%3A+%7B%22%24ne%22%3A+%22COMPLETED%22%7D%7D)
  * DOS offset fix [1/2/43/99] -> [LINK](http://fireworks.dash.materialsproject.org/?fw_query=&wf_query=%7B%22nodes%22%3A%7B%22%24in%22%3A%5B67421%2C+172370%2C+175284%2C+273937%2C+321886%2C+329996%2C+366016%2C+367920%2C+271169%2C+271147%2C+269713%2C+280006%2C+279952%2C+318416%2C+427216%2C+474983%2C+477556%2C+486236%2C+507462%2C+469206%2C+543541%2C+544081%2C+655821%2C+655853%2C+676957%2C+697564%2C+653577%2C+1148100%2C+657911%2C+681304%2C+667056%2C+670679%2C+681135%2C+691009%2C+718861%2C+685397%2C+714229%2C+714688%2C+639588%2C+640899%2C+1081308%2C+1081809%2C+1086911%2C+902977%2C+897375%2C+915719%5D%7D%7D)

### 2017-04-11

- continuing with Hark's RUNNING workflows
- additional 32 materials for which to fix DOS offset (rerun GGA Uniform v2)

#### ICSD 2015/12016

```
507 RUNNING workflows (17.7%)
283 FIZZLED workflows (9.9%)
1930 COMPLETED workflows (67.6%)
117 RESERVED workflows (4.1%)
20 DEFUSED workflows (0.7%)
2857 workflows in total
```

### 2017-04-07

- DOS offset fix: all but two workflows done -> [LINK](http://fireworks.dash.materialsproject.org/?fw_query=&wf_query=%7B%22nodes%22%3A%7B%22%24in%22%3A%5B517856%2C914444%5D%7D%7D)
- petretto and montoyjh to matgen_low queue
- Weike: 457 new ICSD 2016 Structures; icsd_id's issue?

#### ICSD 2015/2016

```
1037 RUNNING workflows (43.9%)
198 FIZZLED workflows (8.4%)
991 COMPLETED workflows (41.9%)
117 RESERVED workflows (5.0%)
20 DEFUSED workflows (0.8%)
2363 workflows in total
```

### 2017-04-06

- Balachandran debugging HgMnO3; all others completed
- identified all fw_id's for DOS offset rerun; encoded in fw_query

#### ICSD 2015

```
488 RUNNING workflows (25.6%)
558 FIZZLED workflows (29.2%)
843 COMPLETED workflows (44.2%)
19 DEFUSED workflows (1.0%)
1908 workflows in total
```

- rerunning 31 fizzled Add to SNL tasks -> [LINK](http://fireworks.dash.materialsproject.org/?fw_query=%7B%22fw_id%22%3A+%7B%22%24in%22%3A+%5B1453147%2C+1453155%2C+1453159%2C+1453307%2C+1453451%2C+1453455%2C+1453459%2C+1455075%2C+1455079%2C+1557758%2C+1558010%2C+1558090%2C+1558246%2C+1558334%2C+1558406%2C+1558414%2C+1558418%2C+1558730%2C+1558742%2C+1558754%2C+1559528%2C+1559718%2C+1559722%2C+1559756%2C+1559768%2C+1559808%2C+1559816%2C+1559824%2C+1559972%2C+1560012%5D%7D%7D&wf_query=)
- rerunning 390 fizzled GGA optimize tasks

### 2017-04-05

- prioritizing ICSD calculations
- all but two Balachandran workflows completed
- completed Sunil's workflow (duplicates) -> [LINK](http://fireworks.dash.materialsproject.org/?fw_query=%7B%22spec.snl.about.remarks%22%3A+%22MP+user+submission%22%2C+%22spec.snl.about.authors.email%22%3A+%22sunil.night%40gmail.com%22%7D&wf_query=%7B%22metadata.reduced_cell_formula%22%3A+%22V2O5%22%7D)
- started re-running all GGA Uniform v2 tasks to fix DOS offset -> [LINK](http://fireworks.dash.materialsproject.org/?fw_query=&wf_query=%7B%22nodes%22%3A%7B%22%24in%22%3A%5B374243%2C++445733%2C++445753%2C++391165%2C++460566%2C++391303%2C++446460%2C++391673%2C++391737%2C++447035%2C++447251%2C++447286%2C++447491%2C++448027%2C++390003%2C++448217%2C++448280%2C++448264%2C++390045%2C++450443%2C++443937%2C++453973%2C++453991%2C++444993%2C++474010%2C++474088%2C++474154%2C++456577%2C++475472%2C++456997%2C++457321%2C++1572647%2C++457316%2C++476617%2C++477952%2C++478198%2C++478616%2C++479032%2C++459852%2C++480150%2C++480823%2C++461408%2C++461468%2C++461474%2C++461480%2C++461594%2C++482630%2C++482710%2C++483012%2C++462374%2C++462397%2C++462975%2C++463216%2C++451253%2C++464694%2C++505296%2C++505584%2C++465580%2C++465606%2C++465800%2C++466730%2C++507506%2C++467578%2C++452191%2C++452203%2C++510415%2C++510632%2C++510744%2C++511020%2C++511224%2C++511231%2C++511236%2C++468796%2C++511445%2C++955298%2C++514432%2C++591603%2C++592097%2C++592727%2C++542311%2C++542323%2C++593637%2C++542809%2C++542803%2C++593703%2C++593727%2C++542821%2C++543950%2C++544273%2C++544315%2C++544297%2C++544791%2C++597031%2C++545151%2C++545175%2C++597335%2C++597347%2C++545421%2C++597979%2C++546413%2C++546461%2C++546835%2C++546979%2C++547257%2C++518582%2C++518576%2C++547947%2C++547965%2C++547971%2C++598714%2C++548357%2C++445685%2C++548849%2C++548850%2C++669425%2C++669545%2C++669983%2C++649551%2C++670715%2C++671069%2C++650313%2C++461630%2C++651741%2C++671849%2C++652213%2C++652237%2C++652272%2C++673062%2C++652353%2C++673831%2C++674845%2C++1148100%2C++677877%2C++658676%2C++657713%2C++680859%2C++664297%2C++667603%2C++683419%2C++688663%2C++683762%2C++684326%2C++691825%2C++688165%2C++691963%2C++692001%2C++684939%2C++688229%2C++685093%2C++692266%2C++704153%2C++713926%2C++713760%2C++706714%2C++706913%2C++693694%2C++715264%2C++908072%2C++708512%2C++694380%2C++690939%2C++712151%2C++906149%2C++716756%2C++856073%2C++697455%2C++719706%2C++709192%2C++887867%2C++908108%2C++847499%2C++639308%2C++694792%2C++882011%2C++707253%2C++852419%2C++708658%2C++853548%2C++845387%2C++845403%2C++873647%2C++844877%2C++873155%2C++872333%2C++873055%2C++847283%2C++1081809%2C++894496%2C++903558%2C++888155%2C++894748%2C++914442%2C++1086911%5D%7D%7D)

#### ICSD 2015

```
493 RUNNING workflows (25.8%)
558 FIZZLED workflows (29.2%)
838 COMPLETED workflows (43.9%)
19 DEFUSED workflows (1.0%)
1908 workflows in total
```

### 2017-04-04

- Re2O7 completed, http://fireworks.dash.materialsproject.org/wf/1370872
- GGA Uniform v2 rerun for mp-3318 completed, http://fireworks.dash.materialsproject.org/wf/417029

### 2017-04-03

#### Hark Lee - VW Solid Solution Metal

```
304 RUNNING workflows (24.8%)
16 FIZZLED workflows (1.3%)
813 READY workflows (66.4%)
81 COMPLETED workflows (6.6%)
10 RESERVED workflows (0.8%)
1224 workflows in total
```

#### Silvana Botti - Perovskite Structures (89070)

```
1 RUNNING workflows (0.6%)
59 FIZZLED workflows (35.1%)
108 COMPLETED workflows (64.3%)
168 workflows in total
```

[LINK](http://fireworks.dash.materialsproject.org/?fw_query=&wf_query=%7B%22metadata.submission_group_id%22%3A89070%2C%22state%22%3A%7B%22%24ne%22%3A%22COMPLETED%22%7D%7D)

#### Ram Balachandran - Fuel Cells

```
6 RUNNING workflows (9.2%)
3 FIZZLED workflows (4.6%)
56 COMPLETED workflows (86.2%)
65 workflows in total
```

-> `lpad rerun_fws -i 1653368 1653198`

#### Mark McAdon - Re2O7

http://fireworks.dash.materialsproject.org/wf/1370872 -> almost completed

#### DOS shift for mp-3318

https://github.com/materialsproject/materials_django/issues/419#issuecomment-287863637  
http://fireworks.dash.materialsproject.org/wf/417029


### 2017-03-03

submitted 65 new structures from Balachandran, Janakiraman with remark "proton conducting materials for fuel cells" -> [LINK](http://fireworks.dash.materialsproject.org/?fw_query=%7B%22spec.snl.about.remarks%22%3A+%22proton+conducting+materials+for+fuel+cells%22%7D&wf_query=)


### 2017-02-17

- fworker query (443 fireworks today):

```
{"$or": [ {"spec.snl.about.remarks": {"$in": ["MP user submission"], "$nin": ["new ICSD batch", "Pauling file", "Heusler ABC2 phases"]}}, {"spec.mpsnl.about.remarks": {"$in": ["MP user submission"], "$nin": ["new ICSD batch", "Pauling file", "Heusler ABC2 phases"]}} ], "state": "READY"}
```

### 2017-02-16

- completed 36 READY user-submitted Add-to-SNL tasks

### 2017-02-14

#### Kitchaev Workflows
- 66/77 COMPLETED (85.7%)
- 6/77 FIZZLED (7.8%)
- 1/77 RUNNING (1.3%)
- 4/77 PAUSED (5.2%)

#### Heusler ABC2 Phase
- 5/2371 COMPLETED (0.2%)
- 1576/2371 FIZZLED (66.5%)
- 43/2371 RUNNING (1.8%)
- 747/2371 READY (31.5%)

### 2017-02-07

#### Kitchaev Workflows
- 66/77 COMPLETED Workflows
- 6 FIZZLED
- 1 RUNNING
- 4 PAUSED

#### Heusler ABC2 Phase
- 5/2371 COMPLETED (0.2%)
- 1576/2371 FIZZLED (66.5%)
- 43/2371 RUNNING (1.8%)
- 747/2371 READY (31.5%)

### 2017-02-01

- 66/77 COMPLETED Kitchaev Workflows; 2 RUNNING
- Mark McAdon (DOW): Re2O7, 1370872 RUNNING
- George Yumnam: 1566138 FIZZLED (also 1566120, 1566104, 1566099, 1567504, 1567491) -> RE-RUNNING
  * 1566099 FIZZLED
- [LINK](http://fireworks.dash.materialsproject.org/?fw_query=&wf_query=%7B%22nodes%22%3A%7B%22%24in%22%3A%5B1370872%2C1566138%2C1566120%2C+1566104%2C+1566099%2C+1567504%2C+1567491%2C1563287%2C+1652717%5D%7D%7D)

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

all workflows COMPLETED -> [LINK](http://fireworks.dash.materialsproject.org/?fw_query=&wf_query=%7B%22metadata.submission_group_id%22%3A+118151%7D)

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
