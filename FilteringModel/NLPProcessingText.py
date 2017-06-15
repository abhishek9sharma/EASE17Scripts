__author__ = 'abhisheksh'
from nltk import word_tokenize
import nltk
from Stopwords import StopW
import string
from nltk.corpus import stopwords
from nltk.corpus import wordnet
import os
class PreProcessData:

    def __init__(self,data,opsys):
        self.data=str(data).lower()

        wd=os.getcwd()
        self.StopWList=StopW(wd+'/CONFIG/StopWordListL.txt')


        self.stemmer = nltk.PorterStemmer()
        self.tokens=self.data.split()
        self.tokensorg=self.tokens
        self.RemovePuntuation()
        self.RemoveStopwords()
        self.RemoveNumbers()
        self.DoStemming()



    def RemoveNumbers(self):
        print("##Removing Numbers###")
        tmpokens=[]
        for t in self.tokens:
            #if wordnet.synsets(t):
            if(t.isdigit()):
                 #print("Removed ::"+str(t))
                 pass
            else:
                tmpokens.append(t)
        self.tokens=tmpokens


    def RemoveStopwords(self):
        print("##Removing Stopwords###")
        for t in self.StopWList.wordList:
            if(t in self.tokens):
                while t in self.tokens:
                    self.tokens.remove(t)


    def RemovePuntuation(self):
        tmptokens=[]
        for t in self.tokens:
            if(1==1):
                #temp=t.strip(string.punctuation).strip(' ')
                punctlist = set(string.punctuation)
                temp = ''.join(ch for ch in t if ch not in punctlist)
                if(temp==''):
                    pass
                    #self.tokens.remove(t)
                else:
                    tmptokens.append(temp)
                    #for n,i in enumerate(self.tokens):
                    #    if(i==t):
                    #        self.tokens[n]=temp
            else:
                tmptokens.append(t)
        self.tokens=tmptokens


    def DoStemming(self):
        self.tokens=[self.stemmer.stem(t) for t in self.tokens]

