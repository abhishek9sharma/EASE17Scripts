__author__ = 'abhisheksh'
import os
from ReadMeDoc2 import  ExtractParagraphsFromReadMe
from Paragraph import Paragraph



class CalculateFeatures:
    def __init__(self,readmefolder,outfolder,filterfolder):
        self.filterfolder=filterfolder
        self.infolder=readmefolder
        self.outfolder=outfolder
        self.Paragraphs=[]
        self.labels={}
        self.ExtratctPragraphswithSomeFeatures()




    def ExtratctPragraphswithSomeFeatures(self):
        fileList=os.listdir(self.infolder)
        for readme in fileList:
            try:
                self.Paragraphs=self.Paragraphs+ExtractParagraphsFromReadMe(self.infolder,readme,self.outfolder,self.filterfolder).ParagraphList
            except:
                print("Exception Occured for File " +readme)



'''
readmefolder='../Experiments/HTMLSORG/'
outfolder='../Experiments/PARAGRAPHS/'
filterfolder='../Experiments/FILTEREDRM/'
CalculateFeatures(readmefolder,outfolder,filterfolder)
'''