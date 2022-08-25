import requests


URL = 'http://127.0.0.1:5000/currency/USD/review'
data = {'data': {'currency_name': 'USD', 'rating': 4, 'comment': 'NEW comment'}}
req = requests.post(URL, json=data)

print(req.status_code)