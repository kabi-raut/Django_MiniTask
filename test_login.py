import urllib.request
import urllib.error

try:
    response = urllib.request.urlopen('http://127.0.0.1:8000/accounts/login/', timeout=5)
    print('✅ SUCCESS: Login endpoint is accessible (200 OK)')
    print(f'Status Code: {response.status}')
except urllib.error.HTTPError as e:
    print(f'❌ ERROR: HTTP {e.code} - {e.reason}')
except Exception as e:
    print(f'⚠️ Connection error: {e}')
