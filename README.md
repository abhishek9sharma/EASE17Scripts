# EASE17Scripts

This is a set of scripts w.r.t the paper ["Cataloging GitHub Repositories"](http://dl.acm.org/citation.cfm?doid=3084226.3084287)
Please use proper citations if you use the [code](https://github.com/abhishek9sharma/EASE17Scripts) or [data](https://github.com/abhishek9sharma/abhishek9sharma.github.io/tree/master/DataSets/EASE17Paper) w.r.t this project. Please refer to the paper [preprint](https://github.com/abhishek9sharma/abhishek9sharma.github.io/blob/master/Papers/EASE17abhishek_preprint.pdf) or camera ready [version](http://dl.acm.org/citation.cfm?doid=3084226.3084287) for details of citations.


### Download the whole project and then

1. *Python 2.7* should be installed on the system or virtualenv(the code has been verified on *Python 2.7.12*)

2. Using command line, navigate to the folder [EASE17Scripts](https://github.com/abhishek9sharma/EASE17Scripts) (make sure this folder contains the file [README.md](https://github.com/abhishek9sharma/EASE17Scripts/blob/master/README.md)])

3. Install/Configure a virtual environment as follows from the command line (this step may be skipped but it may cause dependency issues on the system) (If already configured go to Step 4) (the *pip* and *python* commands should correspond to *Python 2.7*)
    
    a. Installation 
        
        -- Windows  : pip2 install --user virtualenv
        -- Linux    : python2 -m pip install --user virtualenv
        
    b. Configuration (*ease2017* is the environment name)
        
        i. Create
            -- Windows  : python2 -m virtualenv ease2017
            -- Linux    : python2 -m virtualenv ease2017 
        
        ii.  Activate 
            -- Windows  : .\ease2017\Scripts\activate
            -- Linux    :  source ease2017/bin/activate 
        
    c. Install dependencies      
          
        -- Windows  : pip2 install -r requirements.txt
        -- Linux    : pip2 install -r requirements.txt 
    
 4. **Ignore this step if coming from Step 3** else continue to *Activate virtual environment* (*testassignment* is the environment name)
        
        -- Windows  : .\ease2017\Scripts\activate
        -- Linux    :  source ease2017/bin/activate 

5. Delete all files in the folder [Experiments](https://github.com/abhishek9sharma/EASE17Scripts/tree/master/Experiments)

6. *In case you have your own preprocessed documents on which you want to run GALDA place your documents in the folder [PREPROCESSED](https://github.com/abhishek9sharma/EASE17Scripts/tree/master/Experiments/FILTEREDRM/PREPROCESSED) and proceed to Step 7. If you want to collect *GitHub Readme* data then run the [RunExp.py](https://github.com/abhishek9sharma/EASE17Scripts/blob/master/RunExp.py) to extract preprocessed text from functionally descriptive segments in README files (for details of approach please see the  paper [preprint](https://github.com/abhishek9sharma/abhishek9sharma.github.io/blob/master/Papers/EASE17abhishek_preprint.pdf) or camera ready [version](http://dl.acm.org/citation.cfm?doid=3084226.3084287)).

   In case you have your own project list please change the file [Combined_Data_Sample.csv](https://github.com/abhishek9sharma/EASE17Scripts/blob/master/CONFIG/Combined_Data_Sample.csv) with your own files. You may use
   [SelectGitHubRepos.py](https://github.com/abhishek9sharma/EASE17Scripts/blob/master/SelectGitHubRepos.py) to download projects based on certain criteria.

7. Run the [Tune_GALDA.py](https://github.com/abhishek9sharma/EASE17Scripts/blob/master/GALDA/Tune_GALDA.py)
After the above steps if no exeption occurs you can find the topics of input files at [comb2desc.csv](https://github.com/abhishek9sharma/EASE17Scripts/blob/master/Experiments/REPOPROPS/comb2desc.csv)

8. To see a visualization of the created topic model at [VizLDA.ipynb](http://nbviewer.jupyter.org/github/abhishek9sharma/EASE17Scripts/blob/bec18fc1bc4b964d889752d7cb8b534973d887ba/VizLDA.ipynb)

###### Currently tested on Python 2.7.12




