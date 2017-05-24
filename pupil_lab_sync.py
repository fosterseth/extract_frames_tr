import sys, os, subprocess, shutil
import numpy

def main():
    video_filename = sys.argv[1]
    timestamps_filename = sys.argv[2]
    output_filename = sys.argv[3]
    output_timestamps_filename = sys.argv[4]
    
    frame_time = 1 / 30.0

    tmp1 = output_filename + ".tmp"
    if not os.path.exists(tmp1):
        os.mkdir(tmp1)

    command = "ffmpeg -i " + video_filename + " -f image2 -qscale:v 5 " + tmp1 + "\%d.jpg"
    print(command)
    subprocess.call(command.split(' '))
    
    # tmp2 = output_filename + ".tmp2"
    # if not os.path.exists(tmp2):
        # os.mkdir(tmp2)
        
    timestamps = numpy.fromfile(timestamps_filename, dtype='>f8')
    timestamps.tofile(output_timestamps_filename, "\n", "%s")
    timestamps = timestamps - timestamps[0]
    curr_time = 0.0
    curr_image = 1
    fid = open(output_filename + '.ffconcat', 'w')
    fid.write("ffconcat version 1.0\n")
    while curr_time <= timestamps[-1]:
        idx = numpy.argmin(numpy.absolute(timestamps-curr_time))
        curr_time += frame_time
        fid.write("file %s/%d.jpg" % (tmp1, (idx+1)) + "\n")
        fid.write("duration 0.033\n")
        # src = tmp1 + "\\" + "%d.jpg" % (idx+1)
        # dest = tmp2 + "\\" + "%d.jpg" % curr_image
        curr_image += 1
        # shutil.copy(src, dest)
    fid.write("file %s/%d.jpg" % (tmp1, (idx+1)) + "\n")
    fid.close()
        
    command = "ffmpeg -f concat -i " + output_filename + ".ffconcat -pix_fmt yuv420p -vcodec mpeg4 -qscale:v 8 -r 30 " + output_filename
    subprocess.call(command.split(' '))

if __name__ == "__main__":
    main()