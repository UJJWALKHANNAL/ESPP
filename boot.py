import network
import json
import time
import machine
from machine import Pin

# LED to indicate Wi-Fi status
led = Pin(2, Pin.OUT)

# Load Wi-Fi credentials from config.json
def load_config():
    try:
        with open("config.json") as f:
            return json.load(f)
    except Exception as e:
        print("Error loading config:", e)
        return None

# Save Wi-Fi credentials to config.json
def save_config(ssid, password):
    try:
        with open("config.json", "w") as f:
            json.dump({"ssid": ssid, "password": password}, f)
    except Exception as e:
        print("Error saving config:", e)

# Connect to Wi-Fi
def connect_to_wifi():
    config = load_config()
    
    if not config or not config.get("ssid") or not config.get("password"):
        print("No valid Wi-Fi config found, starting AP...")
        start_ap_mode()  # Start Hotspot if no config found
        return False
    
    ssid = config.get("ssid")
    password = config.get("password")
    
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    
    if not wlan.isconnected():
        print(f"Connecting to {ssid}...")
        wlan.connect(ssid, password)
        
        timeout = 10
        while not wlan.isconnected() and timeout > 0:
            time.sleep(1)
            timeout -= 1
    
    if wlan.isconnected():
        print("Wi-Fi connected!")
        print("IP Address:", wlan.ifconfig()[0])
        led.off()  # LED OFF when connected
        return True
    else:
        print("Failed to connect, starting AP...")
        start_ap_mode()
        return False

# Start Hotspot (AP Mode)
def start_ap_mode():
    ap = network.WLAN(network.AP_IF)
    ap.active(True)
    ap.config(essid="ESP_SETUP", authmode=network.AUTH_OPEN)  # Open Hotspot
    print("Hotspot Started! Connect to 'ESP_SETUP' to configure Wi-Fi.")
    led.on()  # LED ON when AP mode is active

# Main Execution
if not connect_to_wifi():
    import main
# 


