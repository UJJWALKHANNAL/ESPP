import machine
import time

# Configure Pin 0 as output
pin = machine.Pin(0, machine.Pin.OUT)

# Blink the LED indefinitely
for i in range(1000000000):
    pin.on()
    time.sleep(0.5)
    pin.off()
    time.sleep(0.5)
