import subprocess as sp
import numpy, os, imageio, pylab
from moviepy.editor import VideoFileClip
#
# def main():
#     video_to_tif('/Users/DoctorWatson/IMTEST/MVI_0027.mov')

def video_to_tif(vid_path):
    if vid_path == None:
        vid_path = '/Volumes/Ramjet2/slit_scan/results/MVI_0001.mov'
    new_clip = VideoFileClip('vid_path')
    new_clip.write_images_sequence("/Volumes/Ramjet2/slit_scan/results/mvi_0001/frame%03d.tif")

    return


vid_path = "/Volumes/Ramjet2/slit_scan/results/MVI_0001.mov"
new_clip = VideoFileClip(vid_path)
new_clip.write_images_sequence("/Volumes/Ramjet2/slit_scan/results/mvi_0001/frame%03d.tif")

vid_path = '/Volumes/Ramjet2/slit_scan/results/MVI_0002.mov'
new_clip = VideoFileClip(vid_path)
new_clip.write_images_sequence("/Volumes/Ramjet2/slit_scan/results/mvi_0002/frame%03d.tif")

# ***************** early incarnations of video reading *********************
#
# filename = '/Users/DoctorWatson/IMTEST/DPREELZ.mov'
# vid = imageio.get_reader(filename,  'ffmpeg')
# nums = [10, 287]
# for num in nums:
#     image = vid.get_data(num)
#     fig = pylab.figure()
#     fig.suptitle('image #{}'.format(num), fontsize=20)
#     pylab.imshow(image)
# pylab.show()




# FFMPEG_BIN = "ffmpeg"
#
# command = [ FFMPEG_BIN,
#             '-i', '/Users/DoctorWatson/IMTEST/DPREELZ.mov',
#             '-f', 'image2pipe',
#             '-pix_fmt', 'rgb24',
#             '-vcodec', 'rawvideo', '-']
# pipe = sp.Popen(command, stdout = sp.PIPE, bufsize=10**8)
#
#
# # read 420*360*3 bytes (= 1 frame)
# raw_image = pipe.stdout.read(420*360*3)
# # transform the byte read into a numpy array
# image =  numpy.fromstring(raw_image, dtype='uint8')
# image = image.reshape((360,420,3))
# print image
# # throw away the data in the pipe's buffer.
# pipe.stdout.flush()
# vid_file = '/Users/DoctorWatson/IMTEST/DPREELZ.mov'
# os.system('ffmpeg -i ' + vid_file + ' -s hd720 -r 30 -f image2  image%05d.jpg')



