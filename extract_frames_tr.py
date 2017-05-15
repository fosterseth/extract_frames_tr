import ConfigParser, glob, subprocess, tr_definitions
frames_folder_name = 'cam%02d_frames_p' # cam01_frames_p
def main():
    config = ConfigParser.ConfigParser()
    config.read(tr_definitions.config_name)
    
    toextract = config.get("extractframes", "toextract")
    extract_begin = config.get("extractframes", "begin")
    extract_end = config.get("extractframes", "end")
    
    toextract = toextract.split(",")
    toextract = [x.strip(" ") for x in toextract]
    
    extractduration, extractdatetimes = tr_definitions.time_duration(extract_begin, extract_end)

    for i in range(0, len(toextract)):
        
        videonames = glob.glob('*cam%02d*.*' % int(toextract[i]))
        if len(videonames) > 0:
            outdirframes = frames_folder_name % int(toextract[i])
            tr_definitions.make_folder_bak(outdirframes)
            videoname = videonames[0] # grab first video in the list
            extract_starttime_str = extractdatetimes[0].strftime('%H:%M:%S.%f')
            subcommand = ' -t ' + extractduration + ' -an -qscale:v 2 -r 30 -f image2' + ' -vf scale=-1:480 ' + outdirframes + '\img_%d.jpg'
            command = 'ffmpeg -ss ' + extract_starttime_str + ' -i ' + videoname + subcommand
            print(command)
            subprocess.call(command.split(' '))            
            
            
if __name__ == "__main__":
    main()