import numpy as np
from sklearn import feature_extraction
from sklearn.feature_extraction.text import CountVectorizer
from pyevolve import G1DList
from pyevolve import GSimpleGA
from pyevolve import Crossovers
import numpy as np
import os
from gensim import corpora, models, interfaces
import gensim
from itertools import izip
from joblib import Parallel, delayed
import multiprocessing
from multiprocessing import Process, Manager
from threading import Thread
import scipy.spatial



foldermain = '../Experiments'
foldername = foldermain + '/FILTEREDRM/PREPROCESSED/'
foldermodels = foldermain + '/MODELS/'


clu2orig={}
docTopicProbMat=None
#COMPUTE BASIC CORPUS AND STUFF
corpus = []
fileList = os.listdir(foldername)
count = 0
corpus = []
texts = []
rc = 0
for f in fileList:
    if (rc % 10 == 0):
        print("Processed ::" + str(rc) + ":: Files ")
    f = open(foldername + f, 'r')
    txt = str(f.read())
    corpus.append(txt)
    texts.append(txt.split())
    rc += 1

dictionary = corpora.Dictionary(texts)
corpus2 = [dictionary.doc2bow(text) for text in texts]
dictionary.save(foldermodels+'MultiCore.dict')
corpora.MmCorpus.serialize(foldermodels+'MultiCoreCorpus.mm', corpus2)

# term frequency
NumApp = len(corpus)
NumFeatures = len(dictionary)
#vectorizer=CountVectorizer(stop_words='english', strip_accents='ascii', max_features=NumFeatures, dtype=np.int32)
vectorizer = CountVectorizer(max_features=NumFeatures, dtype=np.int32)
tf_array = vectorizer.fit_transform(corpus).toarray()
vocab = vectorizer.get_feature_names()


print("Starting Mutations::")
# print(corpus)
print(NumApp)

print(NumFeatures)
NumFeatures = len(vocab)
print(NumFeatures)
print(count)
Centers = []
Clusters = []
classes = []
logfile=open(foldermodels+'/log.txt','w')
sqD=scipy.spatial.distance.squareform(scipy.spatial.distance.pdist(tf_array))

shScore = {}

def CalSilhouette2(j):
    min_b = 10000
    max_a = 0
    clu = classes[j]
    global sqD
    for i in xrange(len(Centers)):
        if i != clu:
            b = np.linalg.norm(Centers[i] - tf_array[j])
            if b < min_b:
                min_b = b

    for k in xrange(len(Clusters[clu])):
        a = sqD[clu2orig[clu][k], j]  # np.linalg.norm(Clusters[clu][k]-tf_array[j])
        if a > max_a:
            max_a = a
    sh = ((min_b - max_a) / max(max_a, min_b))
    if (j % 5000 == 0):
        print("Calclated Silhoute for :" + str(j) + " Documents")
    return sh


topic_num = None

def getTopicProb(j):
    currrdocProb = [0]*topic_num
    for p in docTopicProbMat[j]:
        currrdocProb[p[0]]=p[1]
    return currrdocProb

def eval_func(NTopic):
    global count
    # NTopic[0]=2
    print NTopic[0]
    # LDA
    # model = lda.LDA(n_topics=NTopic[0], n_iter=20,alpha=50.00/NTopic[0],eta=0.01,random_state=12)
    # model.fit(tf_array)
    # doc_topic = model.doc_topic_
    global topic_num
    numoftopics = int(NTopic[0] / 10)
    topic_num = numoftopics
    iters = NTopic[1]
    # al=float(50.00)/float(NTopic[2])
    al = (float(NTopic[2]) - 20) / 480
    bet = (float(NTopic[3]) - 20) / 480
    if al==0.0:
        al = 1/480
    if bet==0.0:
        bet = 1/480
    #al= 0
    #bet = 0

    log=str(count)+' '+str(numoftopics) + ' ' + str(iters) + ' ' + str(al) + ' ' + str(bet) + "\n"
    print log
    logfile.write(log)

    # model=gensim.models.ldamodel.LdaModel(corpus2,num_topics=NTopic[0],id2word=dictionary,iterations=20,alpha=50.00/NTopic[0],eta=0.01)
    # model=gensim.models.ldamulticore.LdaMulticore(corpus2,num_topics=NTopic[0],id2word=dictionary,iterations=20,alpha=50.00/NTopic[0],eta=0.01)
    model = gensim.models.ldamulticore.LdaMulticore(corpus2, num_topics=numoftopics, id2word=dictionary,
                                                    iterations=iters, alpha=al, eta=bet)
    #model = gensim.models.ldamulticore.LdaMulticore(corpus2, num_topics=numoftopics, id2word=dictionary,
    #                                                iterations=iters)

    #model.save(foldermodels+str(log) + '.model')
    print("Created Model::" + str(count))
    doc_topic_list = []
    global docTopicProbMat
    docTopicProbMat=None
    docTopicProbMat = model[corpus2]

    #sequential
    '''
    for l, t in izip(docTopicProbMat, corpus):
        # print t,"#",l
        currrdocProb = []
        for p in l:
            currrdocProb.append(p[1])
            # print(p[1])
        doc_topic_list.append(currrdocProb)

    '''

    pool = multiprocessing.Pool(processes=4)
    doc_topic_list = pool.map(getTopicProb, xrange(len(docTopicProbMat)))
    doc_topic = np.array(doc_topic_list)
    print "********doc topic shape:",doc_topic.shape
    global classes
    classes = []
    for i in range(NumApp):
        try:
            # print("Processing Document "+str(i)+"::"+str(corpus[i]+str(doc_topic[i])))
            classes.append(np.array(doc_topic[i]).argmax())
        except:
            print("Error for Document  " + str(i) + "::" + str(corpus[i] + str(doc_topic[i])))
    classes = np.array(classes)
    # Centroid
    global Centers
    global Clusters
    Centers = []
    Clusters = []
    global clu2orig
    clu2orig={}
    for i in range(numoftopics):
        clu2orig[i] = {}
        tmp_sum = np.zeros((1, NumFeatures))
        cnt = 0
        points = []
        # p = tf_array[classes==i]
        # points = list(p)
        # c_i = p.mean()
        for j in range(NumApp):
            if classes[j] == i:
                points.append(tf_array[j])
                tmp_sum = tmp_sum + tf_array[j]
                clu2orig[i][cnt] = j
                cnt = cnt + 1
        c_i = tmp_sum / cnt
        Centers.append(c_i)
        Clusters.append(points)
        if (len(Clusters) % 100 == 0):
            print(str(len(Clusters)) + " ::: CREATED")

    print(str(len(Clusters)) + " ::: CREATED")
    print("CALCULATING SILHOUEET COFEFFICENT")

    # Silhouette coefficient Compute In Parallel
    s_j = []

    # MULTIPROCESSING
    numofcores = multiprocessing.cpu_count()
    s_j = Parallel(n_jobs=2)(delayed(CalSilhouette2)(j) for j in range(NumApp))

    # MULTITHREADING
    '''
    for j in range(NumApp):
          t = Thread(target=CalSilhouette,args=(j,))
          t.start()
    t.join()
    '''

    '''
    #NORMAL SEQUENTIAL
    for j in range(NumApp):
        min_b=10000
        max_a=0
        clu=classes[j]
        for i in range(len(Centers)):
          if i!=clu:
            b=np.linalg.norm(Centers[i]-tf_array[j])
            if b<min_b:
                min_b=b

        for k in range(len(Clusters[clu])):
            a=np.linalg.norm(Clusters[clu][k]-tf_array[j])
            if a>max_a:
                max_a=a
        s_j.append((min_b-max_a)/max(max_a,min_b))
        print("Cacluated Silhoute for::"+str(len(s_j))+":DOCS:")

    '''
    s = sum(s_j) / NumApp
    s = (s + 1) / 2

    log = "SCORE::" + str(s)
    print log
    logfile.write(log+'\n')
    count = count + 1
    print("COUNT::" + str(count))
    model.clear()
    return s

def eval_func2(NTopic):
    # NTopic[0]=2
    print NTopic[0]
    # LDA
    # model = lda.LDA(n_topics=NTopic[0], n_iter=20,alpha=50.00/NTopic[0],eta=0.01,random_state=12)
    # model.fit(tf_array)
    # doc_topic = model.doc_topic_
    numoftopics = int(NTopic[0] / 10)
    iters = NTopic[1]
    # al=float(50.00)/float(NTopic[2])
    al = (float(NTopic[2]) - 20) / 480
    bet = (float(NTopic[3]) - 20) / 480
    #al = 0
    #bet = 0
    global shScore
    log=str(numoftopics) + ' ' + str(iters) + ' ' + str(al) + ' ' + str(bet) + "\n"
    print log
    if not log in shScore:
        shScore[log] = eval_func(NTopic)
    return shScore[log]


def eval_func_JustModel(NTopic):
    global count
    # NTopic[0]=2
    print NTopic[0]
    # LDA
    # model = lda.LDA(n_topics=NTopic[0], n_iter=20,alpha=50.00/NTopic[0],eta=0.01,random_state=12)
    # model.fit(tf_array)
    # doc_topic = model.doc_topic_
    global topic_num
    numoftopics = int(NTopic[0] / 10)
    topic_num = numoftopics
    iters = NTopic[1]
    # al=float(50.00)/float(NTopic[2])
    al = (float(NTopic[2]) - 20) / 4800
    bet = (float(NTopic[3]) - 20) / 4800

    log=str(count)+' '+str(numoftopics) + ' ' + str(iters) + ' ' + str(al) + ' ' + str(bet) + "\n"
    print log
    logfile.write(log)
    print("Creating Model::" + str(count))
    model = gensim.models.ldamulticore.LdaMulticore(corpus2,passes=20, num_topics=numoftopics, id2word=dictionary,iterations=iters,alpha=al,eta=bet)

    model.save(foldermodels+str(numoftopics) +'_'+str(iters) + '.model')
    #model= gensim.models.ldamodel.LdaModel.load(foldermodels + '44_171.model')
    doc_topic_list = []


genome = G1DList.G1DList(4)
genome.evaluator.set(eval_func2)
genome.setParams(rangemin=20, rangemax=50)
genome.crossover.set(Crossovers.G1DListCrossoverUniform)
ga = GSimpleGA.GSimpleGA(genome)
ga.setPopulationSize(10)
ga.setGenerations(10)
ga.evolve(freq_stats=1)
print ga.bestIndividual()
# print(corpus)
print(NumApp)
#print(NumFeatures)
print(count)
fo = open(foldermodels+"bestindividual", "a")
eval_func_JustModel(ga.bestIndividual().genomeList)
fo.write(str(ga.bestIndividual()))
logfile.write(str(ga.bestIndividual())+'\n')
fo.close()
logfile.close()

try:
    #foldermain = wd + '/Experiments/'
    # folderpath='../EXPERIMENTS/MODELS/'
    folderpath = foldermain + '/MODELS/'

    dictionary = gensim.corpora.Dictionary.load(folderpath + 'MultiCore.dict')
    corpus = gensim.corpora.MmCorpus(folderpath + 'MultiCoreCorpus.mm')
    modelfile = ''
    # for f in os.listdir(folderpath):
    #     if ('.model' in f and '.model.state' not in f):
    #         modelfile = f
    
    for f in os.listdir(folderpath):
        if ('.model' in f):
            filetype = f.split('.')[-1]
            if filetype not in ['state','id2word','npy']:
                modelfile = f

    print(modelfile)
    model_test = gensim.models.ldamodel.LdaModel.load(folderpath + modelfile)

    #

    # In[5]:

    # show word probabilities for each topic
    X = model_test.show_topics(num_topics=50, num_words=5, log=False, formatted=False)
    test = [(x[0], [y[0] for y in x[1]]) for x in X]
    topicDesc = {}

    for t in test:
        topicstr = ' + '.join(str(e) for e in t[1])
        # print topicstr
        topicDesc[t[0]] = topicstr

    model_test.show_topics(num_topics=50, num_words=5, log=False, formatted=False)

    # In[6]:

    # WRITETOFILE
    folder = foldermain + '/REPOPROPS/'

    for k in topicDesc.keys():
        line = str(k) + ',' + topicDesc[k]
        fout = open(folder + 'topickeys.csv', 'a')
        fout.write(line + '\n')
        fout.close()

    # In[7]:

    # LOAD DOCUMENTS
    import os

    foldername = foldermain + '/FILTEREDRM/PREPROCESSED/'
    fileList = os.listdir(foldername)
    docdict = {}
    for fn in fileList:
        f = open(foldername + fn, 'r')
        txt = str(f.read())
        docdict[fn] = txt.split()
        f.close()

    # In[8]:

    # FIND TOPIC
    import numpy as np

    docTopicDict = {}
    for d in docdict.keys():
        docProbs = model_test[[dictionary.doc2bow(docdict[d])]]
        currrdocProb = [0] * 49
        for p in docProbs[0]:
            currrdocProb[p[0]] = p[1]
            doc_topic = np.array(currrdocProb)
            topic = np.array(doc_topic).argmax()
            docTopicDict[d.strip().replace('.txt', '')] = topic

    # In[9]:

    # WRITE DOCTOPIC TO FILES
    folder = foldermain + '/REPOPROPS/'
    for k in docTopicDict:
        line = k + ',' + str(docTopicDict[k])
        fout = open(folder + 'doctopic.csv', 'a')
        fout.write(line + '\n')
        fout.close()

    # In[10]:

    # LOAD DOC/proj/repo NAMEs
    #repdata = os.listdir(foldermain + '/HTMLSORG')
    repdata=os.listdir(foldermain+'/FILTEREDRM/PREPROCESSED/')


    # In[11]:

    # COMBINE DATA
    fnames = docTopicDict.keys()
    cnt = 0
    folder = foldermain + '/REPOPROPS/'
    comb = open(folder + 'comb2desc.csv', 'a')
    for repoline in repdata:
        # fkey=repoline.split(',')[0]
        fkey = repoline.replace('.txt', '')
        if (fkey in fnames):
            currtopic = docTopicDict[fkey]
            newline = repoline.replace('\n', '') + ',' + str(currtopic) + ',' + str(topicDesc[currtopic])
        else:
            newline = repoline.replace('\n', '') + ',TOPICASSIGNED,TOPICWORDS'
        comb.write(newline + '\n')
    comb.close()
except:
    print("Error Occured whil combining topics with documents")


