import machine
import time

# For ESP8266 (NodeMCU) and ESP32 - Built-in LED pin
led = machine.Pin(2, machine.Pin.OUT)  # GPIO2 is default for built-in LED

# Blink LED with 0.5-second interval
while True:
    led.on()  # Turn LED ON
    time.sleep(0.5)
    print("led on")
    led.off()  # Turn LED OFF
    time.sleep(0.5)
    print("led off")
