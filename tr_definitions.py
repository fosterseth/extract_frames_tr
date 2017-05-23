import os, datetime

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
    
def seconds_to_ms(total_seconds):
    if "f" in total_seconds:
        frame_f_rate = total_seconds.split("f")
        total_seconds = float(frame_f_rate[0]) / float(frame_f_rate[1])
        total_seconds = '%.3f' % total_seconds
    if ":" in total_seconds:
        out = total_seconds
    elif "." in total_seconds:
        total_seconds = float(total_seconds)
        m,s = divmod(total_seconds, 60)
        # h,m = divmod(m, 60)
        # return '%d:%d:%.3f' % (h,m,s)
        out = '%02d:%06.3f' % (m,s) # 06 is total width, including decimal
    return out
    