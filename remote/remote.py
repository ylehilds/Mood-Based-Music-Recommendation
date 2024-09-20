from machine import Pin
import network
import urequests
import time
import config
import json

# Button setup
play_btn = Pin(16, Pin.IN, Pin.PULL_DOWN)
pause_btn = Pin(2, Pin.IN, Pin.PULL_DOWN)
skip_btn = Pin(15, Pin.IN, Pin.PULL_DOWN)

# WiFi setup
ssid = config.ssid
password = config.password

wlan = network.WLAN(network.STA_IF)
wlan.disconnect()
wlan.active(True)
wlan.connect(ssid, password)

# Wait for WiFi connection with a timeout
MAX_RETRIES = 10
retries = 0

while not wlan.isconnected() and retries < MAX_RETRIES:
    print("Connecting to WiFi...")
    retries += 1
    time.sleep(1)

if wlan.isconnected():
    print('Connection successful')
    print(wlan.ifconfig())
else:
    print("Failed to connect to WiFi")
    raise RuntimeError("WiFi connection failed")

# Function to trigger IFTTT events
def send_ifttt_event(event_name):
    try:
        request_url = f'https://maker.ifttt.com/trigger/{event_name}/with/key/{config.ifttt_key}'
        res = urequests.post(request_url)
        print(res.text)
        res.close()  # Free up resources by closing the response
    except Exception as e:
        print(f"Error sending {event_name}: {e}")

# Button action functions
def play():
    send_ifttt_event('spotify_play')

def pause():
    send_ifttt_event('spotify_pause')

def skip():
    send_ifttt_event('spotify_skip')

# Debounce time in seconds
DEBOUNCE_TIME = 0.25

try:
    while True:
        if play_btn.value():
            print('play btn pressed')
            play()
            time.sleep(DEBOUNCE_TIME)  # Debouncing

        if pause_btn.value():
            print('pause btn pressed')
            pause()
            time.sleep(DEBOUNCE_TIME)  # Debouncing

        if skip_btn.value():
            print('skip btn pressed')
            skip()
            time.sleep(DEBOUNCE_TIME)  # Debouncing

except Exception as e:
    print(e)
    # Error notification via IFTTT
    request_url = f'https://maker.ifttt.com/trigger/error/with/key/{config.ifttt_key}'
    post_data = json.dumps({"value1": str(e)})
    urequests.post(request_url, headers={'content-type': 'application/json'}, data=post_data)
