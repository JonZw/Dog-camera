import os
import sys

path = sys.argv[1]
name = sys.argv[2]
hostname = os.uname()[1]


os.system('MP4Box -fps 25 -cat '+path+'b-'+ name +'.h264 -cat '+path+'a-'+ name +
          '.h264 -new '+path+name+'-'+hostname+'.mp4 -tmp ~ -quiet')
os.remove(path+'b-'+ name +'.h264')
os.remove(path+'a-'+ name +'.h264')