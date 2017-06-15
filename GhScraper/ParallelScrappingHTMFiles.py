import requests
import urllib2
import re
import codecs
import multiprocessing
from joblib import Parallel, delayed




def ScrapeHTML(link,opfolder):

    link=link.replace('\n','')
    ghprojectinfo = link.split('/')
    opfilename=ghprojectinfo[3] + '_' + ghprojectinfo[4] + '.txt'

    html = ''
    pathfiller='/'

    print("Trying to extract html for  link ::" + link)
    try:
        html = requests.get(link).text
        WTF(html.encode('utf-8'),
                 opfolder + pathfiller + opfilename)
    except:
        try:
            html = urllib2.urlopen(link).read()
            WTF(html.encode('utf-8'),
                     opfolder + pathfiller + opfilename + '.txt')
        except:
            WTF(link, opfolder + pathfiller + opfilename + '_Error.txt')
            html = "Error"
    return html


def WTF(data, filename):
    with open(str(filename), 'a') as fo:
        fo.write(str(data))
        fo.close()


'''

opfolder='../Experiments/HTMLSORG/'
urlfile='../CONFIG/Combined_Data_Sample.csv'
urlList=[]
with open(urlfile, 'r') as f:
    for line in f:
        urlList.append(line)
        #ScrapeHTML(line)


num_cores = multiprocessing.cpu_count()
res=Parallel(n_jobs=num_cores)(delayed(ScrapeHTML)(i) for i in urlList)
'''