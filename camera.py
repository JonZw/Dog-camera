import os
from datetime import datetime
import io
import picamera

secs_before = 10
trigger_fileextension = '.trg'
trigger_path = 'trigger/'
video_path = 'Videos/'

# Format of trigger file name:          2016-08-26-08-05-00.trg


with picamera.PiCamera() as camera:
  camera.resolution = (1920, 1080)
  camera.framerate = 25
#  camera.hflip = True
#  camera.vflip = True
  stream = picamera.PiCameraCircularIO(camera, seconds=(secs_before+10))
  camera.start_recording(stream, format='h264')
  print('Ready for trigger')
  try:
    while True:
      camera.wait_recording(1)
# Look for trigger file
      triggerfiles = [f for f in os.listdir(trigger_path) if f.endswith(trigger_fileextension)]
      if triggerfiles:
        print('Trigger detected!')
# Motion trigger file detected, trim file extension ".trg"
        triggerfile = triggerfiles[0].split('.')[0:1][0]
        print(triggerfile)
# Convert filename to datetime object
        triggertime = datetime.strptime(triggerfile, '%Y-%m-%d-%H-%M-%S')
# Calc seconds to fetch from ringbuffer
        currenttime = datetime.now()
        if triggertime > currenttime:
          triggertime = currenttime
        beforetime = (currenttime - triggertime).total_seconds() + secs_before
        print(beforetime)
# As soon as we detect trigger, split the recording to record the frames "after" trigger
        camera.split_recording(video_path + 'a-' + triggerfile + '.h264')
# Write the seconds "before" trigger to disk as well
        stream.copy_to((video_path + 'b-' + triggerfile + '.h264'), seconds=beforetime)
        stream.clear()
# Wait for trigger to disappear, then split recording back to the in-memory circular buffer
        while os.path.isfile(trigger_path + triggerfiles[0]):
          camera.wait_recording(1)
        print('Trigger stopped!')
        camera.split_recording(stream)
# Start postprocessing
        print('Connect files')
        postprocess = 'python3 postprocess.py '+video_path+' '+triggerfile+' &'
        os.system(postprocess)
        print('Files connected')
  finally:
    camera.stop_recording()