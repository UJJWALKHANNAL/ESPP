import machine
import time

# Configure Pin 0 as output (built-in LED on most ESP modules)
led = machine.Pin(0, machine.Pin.OUT)

# Blink LED with 0.5s interval
while True:
    led.on()  # Turn LED ON
    time.sleep(0.5)
    led.off()  # Turn LED OFF
    time.sleep(0.5)
