import RPi.GPIO as GPIO
import time
import datetime
import os
import mpu6050

trigger_fileextension = '.trg'
trigger_path = 'trigger/'
trigger = ""

# define GPIO mode, pin and use pin as input
GPIO.setmode(GPIO.BOARD)
GPIO_SCL = 2
GPIO_SDA = 3
GPIO.setup(GPIO_SCL, GPIO.OUT)
GPIO.setup(GPIO_SDA, GPIO.IN)

print("MPU started")
print("Waiting for MPU to get idle ...")

# loop until PIR == 0
while GPIO.input(GPIO_SDA) != 0:
    time.sleep(0.2)
print("Now ready for motion detection")

# ToDo: Schwellenwerte definieren (wegen Atmung des Hundes) und dann mittels 1 bzw 0 den motiontrigger von unten anpassen

mpu = mpu6050(0x68)

# while True:
#     print("Temp : "+str(mpu.get_temp()))
#     print()
#
#     #accel_data = mpu.get_accel_data()
#     print("Acc X : "+str(accel_data['x']))
#     print("Acc Y : "+str(accel_data['y']))
#     print("Acc Z : "+str(accel_data['z']))
#     print()
#
#     gyro_data = mpu.get_gyro_data()
#     print("Gyro X : "+str(gyro_data['x']))
#     print("Gyro Y : "+str(gyro_data['y']))
#     print("Gyro Z : "+str(gyro_data['z']))
#     print()
#     print("-------------------------------")
#     time.sleep(1)

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
GPIO.add_event_detect(GPIO_SDA, GPIO.BOTH, callback=MPU_signal)
print("{0:%Y-%m-%d-%H-%M-%S} - Waiting for motion".format(datetime.datetime.now()))

# Main loop
while True:
    time.sleep(60)
