import machine
import time

# Define LED on GPIO2 (built-in LED)
led = machine.Pin(2, machine.Pin.OUT)

# Blink LED every 1 second
while True:
    led.on()
    time.sleep(0.5)
    led.off()
    time.sleep(0.5)
