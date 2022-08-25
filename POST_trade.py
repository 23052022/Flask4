import requests


URL = 'http://127.0.0.1:5000/currency/trade/EURO/USD'
data = {'data': {'amount': 100}}
req = requests.post(URL, json=data)

print(req.status_code)