import time
import datetime
import os
from mpu6050 import mpu6050

trigger_fileextension = '.trg'
trigger_path = 'trigger/'
trigger = ""

# ToDo: Schwellenwerte definieren (wegen Atmung des Hundes) und dann mittels 1 bzw 0 den motiontrigger von unten anpassen

mpu = mpu6050(0x68)

while True:
     print("Temp : "+str(mpu.get_temp()))
     print()

     accel_data = mpu.get_accel_data()
     print("Acc X : "+str(accel_data['x']))
     print("Acc Y : "+str(accel_data['y']))
     print("Acc Z : "+str(accel_data['z']))
     print()

last_trigger = datetime.datetime.now()


# Callback-Function
def MPU_signal():
    global trigger
    global last_trigger
    accel_data = mpu.get_accel_data()  # Alternativ kann gyro auch verwendet werden
    triggertime = datetime.datetime.now()
    if (datetime.datetime.now() - last_trigger).total_seconds() >= 5 * 60:  # 5 minutes have passed since last check
        # set last_trigger time
        last_trigger = datetime.datetime.now()
        try:
            os.remove(trigger_path + trigger + trigger_fileextension)
            print("{0:%Y-%m-%d-%H-%M-%S} - Motion terminated".format(triggertime))
            print()
        except OSError:
            pass

    # Untenstehende Zahlen mit exakten Werten ersetzen
    elif accel_data['x'] > 1 and accel_data['y'] > 1 and accel_data['z'] > 1:  # Falsche Werte(Richtige Werte werden später eingefügt)!!!
        last_trigger = datetime.datetime.now()
        trigger = triggertime.strftime("%Y-%m-%d-%H-%M-%S")
        open(trigger_path + trigger + trigger_fileextension, 'w').close()
        print("{0} - Motion detected".format(trigger))


# Event definition: on gpio state change call MPU_signal function
print("{0:%Y-%m-%d-%H-%M-%S} - Waiting for motion".format(datetime.datetime.now()))

# Main loop
while True:
    MPU_signal()
    time.sleep(30)
