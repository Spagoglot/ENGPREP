import RPi.GPIO as GPIO
import matplotlib.pyplot as plt
import time

comp = 14
dac = [8, 11, 7, 1, 0, 5, 12, 6]
led = [2, 3, 4, 17, 27, 22, 10, 9]
troyka = 13

GPIO.setmode(GPIO.BCM)

GPIO.setup(dac, GPIO.OUT)
GPIO.setup(led, GPIO.OUT)
GPIO.setup(troyka, GPIO.OUT, initial = 1)
GPIO.setup(comp, GPIO.IN)

def num_to_bin(num):
    return [int(i) for i in bin(num)[2:].zfill(8)]

def adc():
    num = 0
    for i in range(7, -1, -1):
        num += 2**i
        GPIO.output(dac, num_to_bin(num))
        time.sleep(0.005)
        comp_val = GPIO.input(comp)
        if (comp_val == 1):
            num -= 2**i
    return num

def comp_to_disco(num):
    str = num_to_bin(num)
    GPIO.output(dac, str)
    return str

data_volts = []

val = 0

GPIO.output(troyka, 1)
time_start = time.time()

while(val < 206):
    val = adc()
    print(val)
    comp_to_disco(val)
    data_volts.append(val)

GPIO.output(troyka, 0)

while (val > 170):
    print(val)
    val = adc()
    comp_to_disco(val)
    data_volts.append(val)

time_end = time.time()

data_times = []

for i in range(0, len(data_volts)):
    t = (time_end - time_start)/len(data_volts)
    data_times.append(i * t)

data_volts_str = [str(i) for i in data_volts]

with open("data.txt", "w") as file:
    file.write("\n".join(data_volts_str))

with open("settings.txt", "w") as file:
    file.write(str((time_end - time_start)/len(data_volts)))
    file.write("\n")
    file.write(str(3.3/256))

plt.plot(data_times, data_volts)
plt.show()