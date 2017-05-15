import ConfigParser, os, shutil, tr_definitions, sys

def main():

    if len(sys.argv) > 1:
        rootletter = sys.argv[1]
        if len(rootletter) != 1:
            raise ValueError("provided drive letter must be one alphabetic letter")
    else:
        rootletter = 'E'

    config = ConfigParser.ConfigParser()
    config.read(tr_definitions.config_name)

    expID = config.get("subinfo", "expID")
    kidID = config.get("subinfo", "kidID")
    dateofexp = config.get("subinfo", "dateofexp")

    filesep = '\\'
    dirprefix = rootletter + ':' + filesep + 'data' + filesep + expID + filesep + filesep + '__' + dateofexp + '_' + kidID

    tr_definitions.make_folder_bak(dirprefix)

    files = os.listdir('.')

    print("copying files to " + dirprefix)
    for f in files:
        print("copying " + f)
        shutil.copy2(f, dirprefix)
    
    
if __name__ == "__main__":
    main()