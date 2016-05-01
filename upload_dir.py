
import os,sys,json
source = sys.argv[1]
f = open("operations.json",'w')
for root,subdirs,files in os.walk(source, topdown=True):
        data = dict()
	data['name'] = os.path.basename(root)
	data['id'] = 0
	data['type'] = 'folder'
	data['children'] = []
        data['files'] = []
	for subdir in subdirs:
		data['children'].append(os.path.basename(subdir))
	for fi in files:
		data['files'].append(os.path.basename(fi))
	json.dump(data, f)
	f.write('\n')
f.close()
