import requests
from flask import Flask, jsonify
app = Flask(__name__)

r = requests.get("https://api.breezometer.com/baqi/?lat=41.9312746&lon=-88.750151&key=30783150517b4bf4865869e94c179134",
                 verify=False)

print r


@app.route('/', methods=['GET'])
def front_page():
    return jsonify(r.json())


if __name__ == '__main__':
    app.run(debug=True, port=8000)