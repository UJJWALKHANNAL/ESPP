import network
import machine
import json
import time

# Load Wi-Fi config
CONFIG_FILE = "wifi_config.json"

# Connect to Wi-Fi
def connect_to_wifi():
    try:
        with open(CONFIG_FILE, "r") as f:
            config = json.load(f)
        
        ssid = config["ssid"]
        password = config["password"]
        
        print(f"Connecting to Wi-Fi: {ssid}")
        
        sta_if = network.WLAN(network.STA_IF)
        sta_if.active(True)
        sta_if.connect(ssid, password)
        
        timeout = 10  # Wait 10 seconds to connect
        while not sta_if.isconnected() and timeout > 0:
            print(".", end="")
            time.sleep(1)
            timeout -= 1
        
        if sta_if.isconnected():
            print("\nWi-Fi connected. IP:", sta_if.ifconfig()[0])
        else:
            print("\nWi-Fi connection failed. Starting Web Setup...")
            import web_setup  # Run web setup if connection fails

    except Exception as e:
        print("Error loading config:", e)
        import web_setup

# Run Wi-Fi connection and updates
connect_to_wifi()

# Run updates automatically
try:
    import update
except:
    print("No updates available.")

