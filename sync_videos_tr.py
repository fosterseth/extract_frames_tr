import ConfigParser, datetime, os, subprocess, sys, tr_definitions, shutil, glob

def main():
    config = ConfigParser.ConfigParser()
    config.read(tr_definitions.config_name)
    
    syncpoints = config.items("syncvideos")
    camID = []
    timestamps = []
    for s in syncpoints:
        if s[0].isdigit():
            camID.append(s[0])
            timestamps.append(s[1])
        elif s[0] == "refid": # ConfigParser makes everything lower-case
            synccamID = s[1]
        elif s[0] == "begin":
            sync_begin = s[1]
        elif s[0] == "end":
            sync_end = s[1]
            
    print(camID)
    print(synccamID)
    print(sync_begin)
    print(sync_end)
    
    if len(sys.argv) > 1:
        tosync = sys.argv[1:]
    else:
        tosync = camID
    
    syncidx = camID.index(synccamID)
    timestamps = [tr_definitions.seconds_to_ms(x) for x in timestamps]
    sync_begin = tr_definitions.seconds_to_ms(sync_begin)
    sync_end = tr_definitions.seconds_to_ms(sync_end)
        
    datetimes = [datetime.datetime.strptime(x, '%M:%S.%f') for x in timestamps]
    syncoffsets = [x-datetimes[syncidx] for x in datetimes]
    sync_begin = datetime.datetime.strptime(sync_begin, '%M:%S.%f')
    sync_end = datetime.datetime.strptime(sync_end, '%M:%S.%f')
    syncduration = str(sync_end - sync_begin)
    
    outdirvideo = "sync"

    tr_definitions.make_folder_bak(outdirvideo)
  
    for i in range(0, len(camID)):
    
        videonames = glob.glob('*cam%02d*.*' % int(camID[i]))
        subcommand = ""
        if len(videonames) > 0 and camID[i] in tosync:
            videoname = videonames[0] # grab first video in the list
            videonameparts = videoname.split('.')
            outputvideoname = videonameparts[0] + '.MOV'
            sync_starttime = sync_begin + syncoffsets[i]
            sync_starttime_str = sync_starttime.strftime('%H:%M:%S.%f')
            
            subcommand = ' -t ' + syncduration + ' -vcodec mpeg4 -qscale:v 5 -r 30 -vf scale=-1:480 -acodec aac -b:a 128k -f mov ' + outdirvideo + '\\' + outputvideoname
            command = 'ffmpeg -ss ' + sync_starttime_str + ' -i ' + videoname + subcommand  

            print(command)
            subprocess.call(command.split(' '))
            
    shutil.copy(tr_definitions.config_name, outdirvideo)
            
            
if __name__ == "__main__":
    main()