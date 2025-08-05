import requests

url = "https://bcb.gov.br/api/servico/sitebcb/indicadorCambio"


response = requests.get(url)

print(response.status_code)
print(response.json())
