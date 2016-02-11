import os, csv, datetime, glob, shutil
import subprocess

'''
extract_frames_tr.py
synchronize videos and extract frames from videos using ffmpeg
ffmpeg must be on the system paths, or be able to be called from this directory
script must be called from the directory containing the subject video files and sync.txt file, for example,

movie_cam01.MOV
movie_cam02.AVI
sync.txt
..
.

Calling the script will create a separate subject directory, e.g.,
X:\multisensory\experiment_12\included\__20151201_12888\
where X is the drive letter of the directory containing the subject video files
The output of ffmpeg will be placed into this directory

Cameras should be denoted with "cam#" (# has width 2 digits, so ..08, 09, 10, 11,..) in their names.
This will determine the folder name of the synced video and extracted frames.

sync.txt is a comma-delimited file including synchronized timing information across the videos
e.g.

#expID,kidID,dateofexp,
12,12888,20151201,
#camID,timestamp,tosync,toextract
1,03:25.773,1,1
2,03:25.734,1,1
3,03:25.423,1,1
#camID,extract_begin,extract_end,
1,01:00.000,2:00.000,
#camID,sync_begin,sync_end,
1,03:50.000,4:50.000,

first 2 lines dictate subject information; experiment ID, KID database ID, and the experiment date in YYYYMMDD format
camID refers to the different cam#_video_r folders
timestamp is a synchronous reference point across the videos.
Meaning, these points should all refer to the same moment in real-time.

tosync and toextract is a 1 or 0 indicating whether to output extracted frames or synchronous video

extract_begin and extract end designate the time range of the extract frames.
This is useful for only extracting a subset of the possible frames.

sync_begin and sync_end designate the time range to sync the videos.

Notes:
camID should always point to the specific camera used to determine the extract/sync time ranges.
In the above example, cam01_video_r was used to determine the range.

this script will also create empty folders and files for camera IDs not in current use, but intended to use later.

When re-running the script, it will move sync.txt from source to destination

'''

def time_duration(t1,t2):
	datetimes = [t1, t2]
	datetimes = [datetime.datetime.strptime(x, '%M:%S.%f') for x in datetimes]
	duration = datetimes[1] - datetimes[0]
	duration = str(duration)
	return duration, datetimes

def copy_if_newer(filename, directory):
	fullfilename = os.path.join(directory, filename)
	if os.path.exists(fullfilename) == True:
		if os.stat(filename).st_mtime - os.stat(fullfilename).st_mtime > 1:
			shutil.copy2(filename, directory)
	else:
		shutil.copy2(filename, directory)

f = open('sync.txt', 'rb')
reader = csv.reader(f)

camID = []
timestamps = []
tosync = []
toextract = []

for row in reader:
	if row[0][0] != "#":
		camID.append(row[0])
		timestamps.append(row[1])
		tosync.append(row[2])
		toextract.append(row[3])

f.close()

expID = camID[0]
kidID = timestamps[0]
dateofexp = tosync[0]

extractcamID = camID[-2]
extract_begin = timestamps[-2]
extract_end = tosync[-2]

synccamID = camID[-1]
sync_begin = timestamps[-1]
sync_end = tosync[-1]

camID = camID[1:-2]
timestamps = timestamps[1:-2]
tosync = tosync[1:-2]
toextract = toextract[1:-2]

refidx = camID.index(extractcamID)
syncidx = camID.index(synccamID)

# convert strings to datetime objects so that offsets can be calculated
datetimes = [datetime.datetime.strptime(x, '%M:%S.%f') for x in timestamps]
extractoffsets = [x-datetimes[refidx] for x in datetimes]
syncoffsets = [x-datetimes[syncidx] for x in datetimes]

extractduration, extractdatetimes = time_duration(extract_begin, extract_end)
syncduration, syncdatetimes = time_duration(sync_begin, sync_end)

indir = os.getcwd()
indir = indir.split('\\')
filesep = '\\'
dirprefix = indir[0] + filesep + 'multisensory' + filesep + 'experiment_' + expID + filesep + 'included' + filesep + '__' + dateofexp + '_' + kidID

if os.path.exists(dirprefix) == False:
	os.makedirs(dirprefix)

allfiles = os.listdir('.')
log = ['cam' not in x for x in allfiles]
fileswithoutcam = [i for(i,v) in zip(allfiles, log) if v]

for f in fileswithoutcam:
	copy_if_newer(f, dirprefix)

for i in range(1,11):
	foldername = dirprefix + filesep + 'cam%02d_frames_p' % int(i)
	if os.path.exists(foldername) == False:
		os.mkdir(foldername)
		
	foldername = dirprefix + filesep + 'cam%02d_video_r' % int(i)
	if os.path.exists(foldername) == False:
		os.mkdir(foldername)

foldername = dirprefix + filesep + 'extra_p'
if os.path.exists(foldername) == False:
	os.mkdir(foldername)

foldername = dirprefix + filesep + 'derived'
if os.path.exists(foldername) == False:
	os.mkdir(foldername)

for i in range(0,len(camID)):
	
	outdirvideo = dirprefix + filesep + 'cam%02d_video_r' % int(camID[i])
	outdirframes = dirprefix + filesep + 'cam%02d_frames_p' % int(camID[i])
	
	# ffmpeg has the ability to have multiple outputs for a single input, which should speed up processing time
	# therefore, the below subcommands are determined and then combined for a single subprocess call to ffmpeg
	if toextract[i] == "1" or tosync[i] == "1":
		videoname = glob.glob('*cam%02d*' % int(camID[i]))[0]
		if len(videoname) > 0:
			extract_starttime = extractdatetimes[0] + extractoffsets[i]
			extract_starttime = extract_starttime.strftime('%H:%M:%S.%f')
			
			sync_starttime = syncdatetimes[0] + syncoffsets[i]
			sync_starttime = sync_starttime.strftime('%H:%M:%S.%f')
		
			subcommand1 = ""
			subcommand2 = ""
			if toextract[i] == "1":
				contents = os.listdir(outdirframes)
				if len(contents) > 1:
					raise ValueError("error on camID %s: frames folders must not already contain files" % camID[i])
				subcommand1 = ' -ss ' + extract_starttime + ' -t ' + extractduration + ' -qscale:v 2 -r 30 -vf scale=-1:480 ' + outdirframes + '\img_%d.jpg'
				
			if tosync[i] == "1":
				contents = os.listdir(outdirvideo)
				if len(contents) > 0:
					raise ValueError("error on camID %s: video folders must not already contain files" % camID[i])
				outputvideoname = videoname.split('.')
				outputvideoname = outputvideoname[0] + '.mov'
				subcommand2 = ' -ss ' + sync_starttime + ' -t ' + syncduration + ' -vcodec mpeg4 -acodec pcm_s16le -qscale:v 2 -r 30 -vf scale=-1:480 ' + outdirvideo + '\\' + outputvideoname
				
			command = 'ffmpeg -i ' + videoname + subcommand1 + subcommand2
			print(command)
			subprocess.call(command.split(' '))
			
			if tosync[i] == "0":
				copy_if_newer(videoname, outdirvideo)