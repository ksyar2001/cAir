import requests

def get_air_data(address):

    address = address.replace(' ', '+').lower()
    request_url = "https://api.breezometer.com/baqi/?location{0}=&key=30783150517b4bf4865869e94c179134".format(address)

    response = requests.get(request_url)