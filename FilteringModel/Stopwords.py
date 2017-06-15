class StopW:
    def __init__(self,filepath):
        self.filepath=filepath
        self.wordList=self.LoadSW()

    def LoadSW(self):
        with open(self.filepath,'r') as f:
            tmpList=f.readlines()
            f.close()
        tmpList=[line.strip() for line in tmpList]
        #print(tmpList)
        return tmpList



