import subprocess
import webbrowser
import time
import os
import requests

# Get the absolute path to the app.py file
app_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'src/app.py'))
app_dir = os.path.dirname(app_path)

# Change the current working directory to the directory containing app.py
os.chdir(app_dir)

# Start the Dash server
try:
    process = subprocess.Popen(['python', 'app.py'])
    print(f"Starting Dash server with {app_path}")
except Exception as e:
    print(f"Failed to start Dash server: {e}")

# Check if the server is running
server_url = 'http://127.0.0.1:8050'
server_running = False
timeout = 60  # Increase timeout to 60 seconds
start_time = time.time()

while time.time() - start_time < timeout:
    if process.poll() is not None:
        print("Dash server process exited prematurely.")
        break
    try:
        response = requests.get(server_url)
        if response.status_code == 200:
            server_running = True
            break
    except requests.ConnectionError as e:
        print(f"Connection error: {e}")
    time.sleep(1)

if server_running:
    # Open the web browser to the Dash app
    try:
        webbrowser.open(server_url)
        print(f"Opening web browser to {server_url}")
    except Exception as e:
        print(f"Failed to open web browser: {e}")

    # Check if the server is still running every 10 seconds
    while True:
        time.sleep(10)
        if process.poll() is None:
            print("Dash server is still running.")
        else:
            print("Dash server exited.")
            break
else:
    print("Failed to start Dash server within the timeout period.")
    if process.poll() is None:
        process.terminate()