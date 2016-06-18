import os,sys,json,random
class uploadTest:
        def __init__(self): 
                self.source = sys.argv[1]
                self.f = open("operations.txt",'w',1)
                self.counter = 0
                print('running')
                self.mapping = dict()
        def getParentID(self,filename):
                #search the dictionary for the filename
                if(filename in self.mapping):
                        return self.mapping[filename]
                else:
                        return -1
        def getNewID(self):
                self.counter += 1
                return self.counter
        def getRandomID(self):
                return random.randrange(0,1000,1)
        def run(self):
                print(self.number_of_operations())
                for root,subdirs,files in os.walk(self.source, topdown=True):
                        #store the root id
                        title = os.path.basename(root)
                        identifier = self.getNewID()
                        pID = self.getParentID(title)
                        if(pID == -1):
                                pID = self.getRandomID()
                        self.f.write(title+','+str(identifier)+','+str(pID)+'\n')
                        for subdir in subdirs:
                                subName = os.path.basename(subdir)
                                self.mapping[subName] = identifier
                        for fi in files:
                                filefolder = os.path.basename(fi)
                                fileID = self.getRandomID()
                                self.f.write(filefolder+','+str(fileID)+','+str(identifier)+'\n')
                        self.f.write('\n')
                print('complete')
                self.f.close()
        def number_of_operations(self):
                count = 0
                for root,subdirs,files in os.walk(self.source, topdown=True):
                        count+=1
                        count= count + len(files)
                return count
if(__name__ == '__main__'):
   var = uploadTest()
   var.run()
