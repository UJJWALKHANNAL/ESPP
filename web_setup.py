import network
import socket
import machine
import json
from boot import save_config
import time

# URL decoding function for MicroPython
def url_decode(s):
    s = s.replace('+', ' ')  # Replace '+' with space
    res = bytearray()
    i = 0
    while i < len(s):
        if s[i] == '%' and i + 2 < len(s):
            try:
                res.append(int(s[i + 1:i + 3], 16))
                i += 3
            except:
                res.append(ord(s[i]))
                i += 1
        else:
            res.append(ord(s[i]))
            i += 1
    return str(res, 'utf-8')

# Start Web Server in AP Mode
def start_web_server():
    addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
    s = socket.socket()
    s.bind(addr)
    s.listen(5)
    print("Web server started. Waiting for connection...")

    while True:
        conn, addr = s.accept()
        print('Client connected from', addr)
        request = conn.recv(1024).decode('utf-8')

        if '/submit?' in request:
            # Extract SSID and password from request
            try:
                params = request.split('/submit?')[1].split(' ')[0]
                ssid = params.split('&')[0].split('=')[1]
                password = params.split('&')[1].split('=')[1]

                # Decode special characters from URL encoding
                ssid = url_decode(ssid)
                password = url_decode(password)

                print(f"New Wi-Fi details received: SSID = {ssid}, PASSWORD = {password}")
                save_config(ssid, password)

                response = "Wi-Fi credentials saved successfully. Restarting ESP..."
                conn.send('HTTP/1.1 200 OK\n')
                conn.send('Content-Type: text/html\n')
                conn.send('Connection: close\n\n')
                conn.send(response)

                time.sleep(2)
                machine.reset()  # Restart ESP to apply new Wi-Fi config
            except Exception as e:
                print("Error processing request:", e)
                conn.send('HTTP/1.1 500 Internal Server Error\n')
                conn.send('Connection: close\n\n')
                conn.send('Failed to update Wi-Fi credentials.')

        else:
            # Serve Wi-Fi Configuration Page
            html = """\
            <html>
            <head>
                <title>ESP Wi-Fi Setup</title>
                <style>
                    body { font-family: Arial; text-align: center; background-color: #f2f2f2; }
                    .container { margin-top: 50px; }
                    input { padding: 10px; width: 80%; }
                    button { padding: 10px; width: 84%; margin-top: 10px; background-color: #4CAF50; color: white; }
                </style>
            </head>
            <body>
                <div class="container">
                    <h2>Configure Wi-Fi</h2>
                    <form action="/submit" method="get">
                        <input type="text" name="ssid" placeholder="Enter Wi-Fi Name (SSID)" required><br>
                        <input type="password" name="password" placeholder="Enter Wi-Fi Password" required><br>
                        <button type="submit">Save & Restart</button>
                    </form>
                </div>
            </body>
            </html>
            """
            conn.send('HTTP/1.1 200 OK\n')
            conn.send('Content-Type: text/html\n')
            conn.send('Connection: close\n\n')
            conn.send(html)

        conn.close()

# Start Web Server
start_web_server()
