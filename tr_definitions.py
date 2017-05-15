import ConfigParser, os, datetime

config_name = "config.ini"

def make_folder_bak(foldername):
    if os.path.exists(foldername) == False:
        os.makedirs(foldername)
    else:
        if len(os.listdir(foldername)) > 0:
            i = 1
            while True:
                bakfoldername = foldername + '_bak%d' % i
                if os.path.exists(bakfoldername) == True:
                    i += 1
                else:
                    break
            os.rename(foldername, bakfoldername)
            os.makedirs(foldername)           
            
def time_duration(t1,t2):
    datetimes = [t1, t2]
    datetimes = [datetime.datetime.strptime(x, '%M:%S.%f') for x in datetimes]
    duration = datetimes[1] - datetimes[0]
    duration = str(duration)
    return duration, datetimes

def make_folder_num(foldername):
    i = 1
    while True:
        foldername_num = foldername + '_%d' % i
        if os.path.exists(foldername_num) == True:
            i += 1
        else:
            break
    os.makedirs(foldername_num)
    return foldername_num
    