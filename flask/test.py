import requests

response = requests.get('http://localhost:5000/api/users')
if response.status_code == 200:
    data = response.json()
    print(data)
else:
    print('Failed to get data')
