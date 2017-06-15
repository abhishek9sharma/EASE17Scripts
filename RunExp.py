__author__ = 'abhisheksh'
import multiprocessing
from GhScraper.ParallelScrappingHTMFiles import ScrapeHTML
import multiprocessing
from joblib import Parallel, delayed
import os
wd = os.getcwd()


#Scrape GITHUB PROJECT HTMLS
opfolder=wd+'/Experiments/HTMLSORG/'
urlfile=wd+'/CONFIG/Combined_Data_Sample.csv' # Your Projects should be in .csv format as  in the sample file mentioned here
urlList=[]
with open(urlfile, 'r') as f:
    for line in f:
        urlList.append(line)
        #ScrapeHTML(line)


num_cores = multiprocessing.cpu_count()
res=Parallel(n_jobs=num_cores)(delayed(ScrapeHTML)(i,opfolder) for i in urlList)


#EXTRACT RELEVANT SEGMENTS FROM README
from FilteringModel.FilterFiles import CalculateFeatures


readmefolder=wd+'/Experiments/HTMLSORG/'
outfolder=wd+'/Experiments/PARAGRAPHS/' #THIS WILL CONTAIN ALL THE TEXT SEGMENTS EXTRACTED FROM README FILE
filterfolder=wd+'/Experiments/FILTEREDRM/' # THIS CONTAINS THE SEGMENT MOST SIMIALR TO DESCRIPTION
CalculateFeatures(readmefolder,outfolder,filterfolder)
# THE IMPUT FILES IN  Experiments/FILTEREDRM/PREPROCESSED ware to be  used for training the LDA MODEL


