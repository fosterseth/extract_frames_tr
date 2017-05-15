import ConfigParser, glob, subprocess, tr_definitions, shutil

def main():
    config = ConfigParser.ConfigParser()
    config.read(tr_definitions.config_name)
    
    totrim = config.get("trimvideos", "totrim")
    trim_begin = config.get("trimvideos", "begin")
    trim_end = config.get("trimvideos", "end")
    
    totrim = totrim.split(",")
    totrim = [x.strip(" ") for x in totrim]
    
    trimduration, trimdatetimes = tr_definitions.time_duration(trim_begin, trim_end)
    outdirvideo = "trim"
    tr_definitions.make_folder_bak(outdirvideo)
    
    for i in range(0, len(totrim)):
        videonames = glob.glob('*cam%02d*.*' % int(totrim[i]))
        if len(videonames) > 0:
            videoname = videonames[0] # grab first video in the list
            subcommand = ' -t ' + trimduration + ' -vcodec mpeg4 -qscale:v 5 -r 30 -vf scale=-1:480 -acodec aac -b:a 128k -f mov ' + outdirvideo + '\\' + videoname
            command = 'ffmpeg -ss ' + trim_begin + ' -i ' + videoname + subcommand  
            print(command)
            subprocess.call(command.split(' '))            
            
    shutil.copy(tr_definitions.config_name, outdirvideo)
    
if __name__ == "__main__":
    main()