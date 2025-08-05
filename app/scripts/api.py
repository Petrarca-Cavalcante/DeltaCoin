import requests

url = 


response = requests.get(url)

print(response.status_code)
print(response.json())
