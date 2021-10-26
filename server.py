import requests

def make_request():
    request = requests.get("http://a0585513.xsph.ru/get")
    response = request.json()
    return response
