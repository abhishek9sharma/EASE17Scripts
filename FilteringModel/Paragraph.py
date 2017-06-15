__author__ = 'abhisheksh'
import nltk.tokenize
from NLPProcessingText import  PreProcessData
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity



class Paragraph:

    def __iter__(self):
        for attr,val in self.__dict__.iteritems():
            yield attr, val

    def __init__(self,text,posindoc,headertext,filename,nofpars,readmedesc,readmefilename):
        self.parentfilename=readmefilename
        self.filename=filename
        self.readmdesc=readmedesc
        self.readmdesc_P=self.PreProcess(self.readmdesc)
        #paragraphpostionfeatures
        self.posindoc=float(posindoc)
        self.relposindoc=float(float(posindoc)/float(nofpars))
        self.relposindocinv=(float(nofpars)-float(posindoc))/float(nofpars)



        #textfeaturesmaintext
        self.maintext=text
        self.nooofwordsinmaintext=len(self.maintext.split())
        self.mainTextProbs={"POS":0,"NEG":0}

        self.PreProcessedmaintext=self.PreProcess(self.maintext)
        self.PreProcessedmainTextProbs={"POS":0,"NEG":0}
        self.nooofwordsinmaintext_P=len(self.PreProcessedmaintext)
        self.mainTextProbs_P={"POS":0,"NEG":0}

        #pargraph header features
        self.headertext=headertext
        self.nooofwordsinheader=len(self.headertext.split())
        self.headertextProbs={"POS":0,"NEG":0}

        self.PreProcessedHeadertext=self.PreProcess(self.headertext)
        self.PreProcessedheadertextProbs={"POS":0,"NEG":0}
        self.nooofwordsinheader_P=len(self.PreProcessedHeadertext)
        self.headertextProbs_P={"POS":0,"NEG":0}
        self.label=-1

        self.SSWithDesc=self.GetSimScore()
        self.SSLabel=-1

        self.SSRPOSLabel=-1
        self.SSWithDescH=self.GetSimScoreH()
        self.SSLabelH=-1


    def PreProcess(self,text):
        pd=PreProcessData(text,'ONLYPREPROCESS')
        print(pd.tokens)
        return " ".join(pd.tokens)

    def GetSimScore(self):
        vect=TfidfVectorizer()
        #tfidmatrix=vect.fit_transform([self.readmdesc,self.maintext])
        tfidmatrix=vect.fit_transform([self.readmdesc_P,self.PreProcessedmaintext])
        cosim=cosine_similarity(tfidmatrix[0:1],tfidmatrix)
        #self.SSWithDesc=cosim[:,1]
        return cosim[:,1][0]

    def GetSimScoreH(self):
        vect=TfidfVectorizer()
        #tfidmatrix=vect.fit_transform([self.readmdesc,self.headertext])
        tfidmatrix=vect.fit_transform([self.readmdesc_P,self.PreProcessedHeadertext])
        cosim=cosine_similarity(tfidmatrix[0:1],tfidmatrix)
        #self.SSWithDesc=cosim[:,1]
        return cosim[:,1][0]


    def StoreMaxMinValues(self,max,min):
        self.MaxDict=max
        self.MinDict=min


    def Normalize(self):

       if(float(self.MaxDict['SSWithDesc']-self.MinDict['SSWithDesc'])==0):
           pass
       else:
           self.SSWithDesc= float(self.SSWithDesc-self.MinDict['SSWithDesc'])/float(self.MaxDict['SSWithDesc']-self.MinDict['SSWithDesc'])
           if(self.SSWithDesc<0):
               print("DEBUGX")


       if(float(self.MaxDict['SSWithDescH']-self.MinDict['SSWithDescH'])==0):
           pass
       else:
           self.SSWithDescH= float(self.SSWithDescH-self.MinDict['SSWithDescH'])/float(self.MaxDict['SSWithDescH']-self.MinDict['SSWithDescH'])
           if(self.SSWithDescH<0):
               print("DEBUGX")



       if(float(int(self.MaxDict['posindoc'])-int(self.MinDict['posindoc']))==0):
            pass
       else:

            orgposin= self.posindoc
            self.posindoc=float(int(self.posindoc)-int(self.MinDict['posindoc']))/float(int(self.MaxDict['posindoc'])-int(self.MinDict['posindoc']))
            if(self.posindoc<0):
               print("DEBUGX")





