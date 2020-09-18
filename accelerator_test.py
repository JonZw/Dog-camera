from mpu6050 import mpu6050

mpu = mpu6050(0x68)

#Just for testing the output, will be removed later 
while True:
     print("Temp : "+str(mpu.get_temp()))
     print()

     accel_data = mpu.get_accel_data()
     print("Acc X : "+str(accel_data['x']))
     print("Acc Y : "+str(accel_data['y']))
     print("Acc Z : "+str(accel_data['z']))
     print()