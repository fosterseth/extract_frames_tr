import shutil, csv

f = open('sync.txt', 'rb')
reader = csv.reader(f)

line = reader.next()
line = reader.next()
expID = line[0]
kidID = line[1]
dateofexp = line[2]

f.close()

newdirectory = 'z:\\data\\' + expID + '\\__' + dateofexp + '_' + kidID

print("copying files, please do not close")
shutil.copytree('.', newdirectory)
print("copying finished")