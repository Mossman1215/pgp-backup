import os,sys,json,random
class uploadTest:
        def __init__(self): 
                self.source = sys.argv[1]
                self.f = open("operation_inst.json",'w')
                self.counter = 0
                print('running')
        def getFileID(filename,self):
                #search the file for an existing number
                f2 = open('operation_inst.json','r')
                for line in f2:
                        line_arr = line.split(',')
                        if(filename == line_arr[0]):
                                f2.close()
                                return int(line_arr[2])
                f2.close()
                return -1
        def getNewID(self):
                self.counter += 1
                return self.counter
        def getRandomID(self):
                return random.randint(100,10000)
        def run(self):
                for root,subdirs,files in os.walk(self.source, topdown=True):
                        #store the root id
                        title = os.path.basename(root)
                        rootID = self.getFileID(title)
                        if(rootID == -1):
                                rootID = self.getNewID()
                        self.f.write(title+','+'0'+','+str(rootID)+'\n')
                                # every folder and file is parented to this id
                        for subdir in subdirs:
                                namefolder = os.path.basename(subdir)
                                folderID = self.getFileID(namefolder)
                                if(folderID == -1):
                                        folderID = self.getNewID()
                                self.f.write(namefolder+','+str(folderID)+','+str(rootID)+'\n')
                        for fi in files:
                                filefolder = os.path.basename(fi)
                                fileID = self.getFileID(filefolder)
                                if(folderID == -1):
                                        fileID = self.getRandomID()
                                self.f.write(filefolder+','+str(fileID)+','+str(rootID)+'\n')
                        self.f.write('\n')
                print('complete')
                self.f.close()
if(__name__ == '__main__'):
   var = uploadTest()
   var.run()
