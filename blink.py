>>> import machine
>>> import time
>>> pin = machine.Pin(0, machine.Pin.OUT)
>>> for i in range(1000000000):
...     pin.on()
...     time.sleep(0.5)
...     pin.off()
...     time.sleep(0.5)
...
