__author__ = 'abhisheksh'
import re
from bs4 import BeautifulSoup
import random
import os
import re
from Paragraph import Paragraph

class ExtractParagraphsFromReadMe:
    def __init__(self,readmefolder,filename,parfolder,filterfolder):
        self.inf=readmefolder
        self.infile=filename
        self.filF=filterfolder
        self.dirparheaderbased=parfolder
        self.ParagraphList=[]
        self.ExtractReadme()
        self.TTW=''
        self.TTW_P=''
        self.SetSimScoreLabels()
        self.SetSimScoreLabelsH()
        self.SetSimScoreRPOSLabels()
        self.MaxDict={}
        self.MinDict={}

        '''
        if(len(self.ParagraphList)>0):
            self.FindMaxMinForEachFeature()
            self.UpdateEachParObjectWithMAxMinValues()

        '''

        if(len(self.TTW)>0):
            fout=open(self.filF+'RAW/'+self.infile,'a')
            fout.write(self.TTW)
            fout.close()

            fout_P=open(self.filF+'PREPROCESSED/'+self.infile,'a')
            fout_P.write(self.TTW_P)
            fout_P.close()

        #self.NormalizePos()


    def ExtractReadme(self):
             htmlfile=open(self.inf+'//'+self.infile,'r')
             html=htmlfile.read()
             htmlfile.close()
             regexcodremover= r'<code>.*?</code>'
             html=re.sub(regexcodremover,'',html)
             soup = BeautifulSoup(html,"html.parser")
             self.readmedesc=soup.find("title").text
             readmesoup=soup.find("div", {"id": "readme"})
             for script in readmesoup(["script", "style"]):
                 script.extract()
             self.ExtractHeaderData(readmesoup,self.infile)


    def ExtractHeaderData(self,soup,infile):
        allelements=soup.findAll()
        counth=len(soup.findAll('h1'))+len(soup.findAll('h2'))+len(soup.findAll('h3'))+len(soup.findAll('h4'))+len(soup.findAll('h5'))+len(soup.findAll('h6'))
        headerDict={}
        currheader='h100'
        frstheader=False
        cntprocessed=0
        if(counth>0):
            for e in allelements:
                if(e.name in ['h1','h2','h3','h4','h5','h6']):
                    #headerfound=True
                    if(not(cntprocessed==0)):
                        currheader=e.text
                        #currheader=currheader+"_SEP_"+str(cntprocessed)
                        headerDict[currheader]=['',0,'']
                        cntprocessed+=1
                        frstheader=False
                    else:
                        cntprocessed+=1
                        frstheader=True
                else:
                    if(not(frstheader)):
                        if(e.text.strip() not in headerDict[currheader][0]):
                            headerDict[currheader][0]= headerDict[currheader][0]+" "+e.text.strip()
                            headerDict[currheader][1]=cntprocessed
                            headerDict[currheader][2]=currheader
                    #headerfound=False
        else:
            self.headerDict['Noheaderfound']=[soup.get_text(),0,'']

        count=0
        for k,v in headerDict.iteritems():
            filename=infile.replace('.txt','')+'_'+str(count)+'.txt'
            fout=open(self.dirparheaderbased+filename,'a')
            #headername=str(k).split('_SEP_')[0]
            headername=k
            fout.write(headername+'\n'+headerDict[k][0])
            fout.close()
            #self.ParagraphDict[filename]=[headername+'\n'+headerDict[k][0]headerDict[k][1],headername]
            #self.WritePar(headername,headername+'\n'+headerDict[k][0],filename)
            try:
                self.CalculateFeatures(filename,str(headerDict[k][1]),headername,headername+'\n'+headerDict[k][0],len(headerDict))
            except:
                print("exception")
            count+=1


    def CalculateFeatures(self,filename,paragraphpos,headername,text,nofpars):
        featurerow=filename+","+paragraphpos+','+headername
        pg=Paragraph(text,paragraphpos,headername,filename,nofpars,self.readmedesc,self.infile)
        self.ParagraphList.append(pg)
        #print(featurerow)

    def WritePar(self,headername,text,filename):
         fout=open(self.dirparheaderbased+filename,'a')
         fout.write(headername+'\n'+text)
         fout.close()


    def SetSimScoreLabels(self):
         maxscore=-1000
         for pg in self.ParagraphList:
             if(pg.SSWithDesc>maxscore):
                 maxscore=pg.SSWithDesc
             else:
                 pass

         for pg in self.ParagraphList:
             if(pg.SSWithDesc>=maxscore):
                 pg.SSLabel=1
                 self.TTW=self.TTW+ ' '+pg.maintext
                 self.TTW_P=self.TTW_P+ ' '+pg.PreProcessedmaintext
             else:
                 pg.SSLabel=0


    def SetSimScoreRPOSLabels(self):
         maxscore=-1000
         for pg in self.ParagraphList:
             if((float(pg.SSWithDesc)+float(pg.relposindocinv))>maxscore):
                 maxscore=(float(pg.SSWithDesc)+float(pg.relposindocinv))
             else:
                 pass

         for pg in self.ParagraphList:
             if((float(pg.SSWithDesc)+float(pg.relposindocinv))>=maxscore):
                 pg.SSRPOSLabel=1
                 #self.TTW=self.TTW+ ' '+pg.maintext
                 #self.TTW_P=self.TTW_P+ ' '+pg.PreProcessedmaintext
             else:
                 pg.SSRPOSLabel=0



    def SetSimScoreLabelsH(self):
         maxscoreH=-1000
         for pg in self.ParagraphList:
             if(pg.SSWithDescH>=maxscoreH):
                 maxscoreH=pg.SSWithDescH
             else:
                 pass

         for pg in self.ParagraphList:
             if(pg.SSWithDescH>=maxscoreH):
                 pg.SSLabelH=1
             else:
                 pg.SSLabelH=0


    def FindMaxMinForEachFeature(self):
        ClassSpecFeatures=dict((self.ParagraphList[0]))
        if(self.infile=='adammeghji_ansible-ltc-mining-on-ec2.txt'):
            print("DEBUG")

        for k in ClassSpecFeatures.keys():
            try:
                kvals=[float(getattr(i,k)) for i in self.ParagraphList]
                self.MaxDict[k]=max(kvals)
                self.MinDict[k]=min(kvals)
                if(self.MinDict[k]>self.MaxDict[k]):
                    print("DEBUG")
            except:
                self.MaxDict[k]=0
                self.MinDict[k]=0

                #self.MaxDict[k]=ClassSpecFeatures[k]
            #self.MinDict[k]=ClassSpecFeatures[k]

        '''
        for k in ClassSpecFeatures:
            self.MaxDict[k]=max([i.getattr(self,k) for i in self.ParagraphList])

            for pg in self.ParagraphList:
                pgtempdict=dict(pg)
                if(pgtempdict[k]>self.MaxDict[k]):
                    self.MaxDict[k]=pgtempdict[k]
                else:
                    pass

                if(pgtempdict[k]<self.MinDict[k]):
                    self.MinDict[k]=pgtempdict[k]
                else:
                    pass
        '''


    def UpdateEachParObjectWithMAxMinValues(self):
        for pg in self.ParagraphList:
            pg.StoreMaxMinValues(self.MaxDict,self.MinDict)


    def NormalizePos(self):
        for pg in self.ParagraphList:
            pg.Normalize()





