import ConfigParser, datetime, glob, subprocess, sys, tr_definitions, shutil
frames_folder_name = 'cam%02d_frames_p' # cam01_frames_p
def main():
    config = ConfigParser.ConfigParser()
    config.read(tr_definitions.config_name)
    
    testpoints = config.items("syncvideos")
    camID = []
    timestamps = []
        
    for s in testpoints:
        if s[0].isdigit():
            camID.append(s[0])
            timestamps.append(s[1])
        elif s[0] == "refid": # ConfigParser makes everything lower-case
            testcamID = s[1]
        elif s[0] == "begin":
            test_begin = s[1]
        elif s[0] == "end":
            test_end = s[1]
            
    if len(sys.argv) > 1:
        toextract = sys.argv[1:]
    else:
        toextract = camID
    
    print(camID)
    print(testcamID)
    print(test_begin)
    print(test_end)
    
    testidx = camID.index(testcamID)
    datetimes = [datetime.datetime.strptime(x, '%M:%S.%f') for x in timestamps]
    testoffsets = [x-datetimes[testidx] for x in datetimes]
    print(testoffsets)
    testduration, testdatetimes = tr_definitions.time_duration(test_begin, test_end)
  
    for i in range(0, len(camID)):
        
        videonames = glob.glob('*cam%02d*.*' % int(camID[i]))
        if len(videonames) > 0 and camID[i] in toextract:
            outdirframes = frames_folder_name % int(camID[i])
            tr_definitions.make_folder_bak(outdirframes)
            videoname = videonames[0] # grab first video in the list
            videonameparts = videoname.split('.')
            outputvideoname = videonameparts[0] + '.MOV'
            test_starttime = testdatetimes[0] + testoffsets[i]
            test_starttime_str = test_starttime.strftime('%H:%M:%S.%f')
            
            subcommand = ' -t ' + testduration + ' -an -qscale:v 2 -r 30 -f image2' + ' -vf scale=-1:480 ' + outdirframes + '\img_%d.jpg'
            command = 'ffmpeg -ss ' + test_starttime_str + ' -i ' + videoname + subcommand  

            print(command)
            subprocess.call(command.split(' '))
                  
if __name__ == "__main__":
    main()