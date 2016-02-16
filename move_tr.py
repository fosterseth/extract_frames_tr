import ConfigParser, os, glob, shutil, extract_frames_tr

config = ConfigParser.ConfigParser()
config.read("config.ini")

expID = config.get("subinfo", "expID")
kidID = config.get("subinfo", "kidID")
dateofexp = config.get("subinfo", "dateofexp")

indir = os.getcwd()
indir = indir.split('\\')
filesep = '\\'
dirprefix = indir[0] + filesep + 'multisensory' + filesep + 'experiment_' + expID + filesep + 'included' + filesep + '__' + dateofexp + '_' + kidID

extract_frames_tr.make_folder_bak(dirprefix)

camfiles = glob.glob('*cam*.*')
bakfiles = glob.glob('*bak*')

files = os.listdir('.')
files = [x for x in files if x not in camfiles and x not in bakfiles]

for f in files:
	shutil.move(f, dirprefix)