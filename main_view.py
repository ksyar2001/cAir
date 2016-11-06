import requests
from flask import Flask, render_template, request
app = Flask(__name__)

r = requests.get("https://api.breezometer.com/baqi/?location=west+lincoln+highway,+dekalb,+il,+united+states&key=30783150517b4bf4865869e94c179134",
                 verify=False)
# print r.json()


@app.route('/', methods=['GET'])
def front_page():
    return render_template('front_page.html')


@app.route('/map/', methods=['POST'])
def hello():
    if request.method == 'POST':
        address = (request.form["location"]).replace(' ', '+').lower()
        request_url = "https://api.breezometer.com/baqi/?location={0}&key=30783150517b4bf4865869e94c179134".format(address)
        response = requests.get(request_url, verify=False)
        json_response = response.json()

        air_quality = json_response["breezometer_description"]
        air_quality_color = json_response["breezometer_color"]

        geocode_url = "https://maps.googleapis.com/maps/api/geocode/json?address={0}&key=AIzaSyCLkcGTP4IbCPKTMsiaEgFoIKyDsUjMnZA".format(address)
        map_response = requests.get(geocode_url)
        map_response_json = map_response.json()

        lat = map_response_json["results"][0]["geometry"]["location"]["lat"]
        lng = map_response_json["results"][0]["geometry"]["location"]["lng"]

        return render_template("map_page.html", air_quality=air_quality, air_color=air_quality_color, lat=lat, lng=lng)


if __name__ == '__main__':
    app.run(debug=True, port=8000)