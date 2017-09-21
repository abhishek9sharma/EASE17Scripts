# EASE17Scripts

This is a set of scripts w.r.t the paper ["Cataloging GitHub Repositories"](http://dl.acm.org/citation.cfm?doid=3084226.3084287)
Please use proper citations if you use the [code](https://github.com/abhishek9sharma/EASE17Scripts) or [data](https://github.com/abhishek9sharma/abhishek9sharma.github.io/tree/master/DataSets/EASE17Paper) w.r.t this project. Please refer to the paper [preprint](https://github.com/abhishek9sharma/abhishek9sharma.github.io/blob/master/Papers/EASE17abhishek_preprint.pdf) or camera ready [version](http://dl.acm.org/citation.cfm?doid=3084226.3084287) for details of citations.


### Download the whole project and then

##### 1. Delete all files in the folder [Experiments](https://github.com/abhishek9sharma/EASE17Scripts/tree/master/Experiments)

##### 2.Run the [RunExp.py](https://github.com/abhishek9sharma/EASE17Scripts/blob/master/RunExp.py) to extract preprocessed text from functionally descriptvie segments in README files (for details of approach please see the  paper [preprint](https://github.com/abhishek9sharma/abhishek9sharma.github.io/blob/master/Papers/EASE17abhishek_preprint.pdf) or camera ready [version](http://dl.acm.org/citation.cfm?doid=3084226.3084287)).

   In case you have your own projects please change the file [Combined_Data_Sample.csv](https://github.com/abhishek9sharma/EASE17Scripts/blob/master/CONFIG/Combined_Data_Sample.csv) with your own files.
##### 3.Run the [Tune_GALDA.py](https://github.com/abhishek9sharma/EASE17Scripts/blob/master/GALDA/Tune_GALDA.py)

After the above steps if no exeption occurs you can find the topics of imput files at [comb2desc.csv](https://github.com/abhishek9sharma/EASE17Scripts/blob/master/Experiments/REPOPROPS/comb2desc.csv)

You can see a visualization of the created topic model at [VizLDA.ipynb](http://nbviewer.jupyter.org/github/abhishek9sharma/EASE17Scripts/blob/bec18fc1bc4b964d889752d7cb8b534973d887ba/VizLDA.ipynb)

###### Currently tested on Python 2.7.6




