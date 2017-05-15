import ConfigParser, glob, subprocess, os, sys, tr_definitions
main_audio_folder_name = 'speech_r'
sub_audio_folder_name = 'speech_r\sub'
def main():
    config = ConfigParser.ConfigParser()
    config.read(tr_definitions.config_name)

    if len(sys.argv) == 1:
        toextract = config.get("extractaudio", "toextract")
        toextract = toextract.split(",")
        toextract = [x.strip(" ") for x in toextract]
    else:
        toextract = sys.argv[1:]
        
    first_audio = True
    print(toextract)
    for a in range(0, len(toextract)): 
        videonames = glob.glob('*cam%02d*.*' % int(toextract[a]))
        if len(videonames) > 0:
            if first_audio:
                if os.path.exists(main_audio_folder_name) == False:
                    os.mkdir(main_audio_folder_name)
                if os.path.exists(sub_audio_folder_name) == False:
                    os.mkdir(sub_audio_folder_name)
                outdiraudio = main_audio_folder_name
                first_audio = False
            else:
                outdiraudio = sub_audio_folder_name
            videoname = videonames[0] 
            outputaudioname = videoname.split('.')
            outputaudioname = outputaudioname[0] + '.wav'
            subcommand = ' -vn -f wav ' + outdiraudio + '\\' + outputaudioname
            command = 'ffmpeg -y -i ' + videoname + subcommand
            print(command)
            subprocess.call(command.split(' '))  
                   
if __name__ == "__main__":
    main()
