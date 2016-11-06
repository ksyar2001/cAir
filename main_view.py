import requests
import json
from flask import Flask, render_template, request
app = Flask(__name__)

r = requests.get("https://api.breezometer.com/baqi/?location=west+lincoln+highway,+dekalb,+il,+united+states&key=30783150517b4bf4865869e94c179134",
                 verify=False)
# print r.json()


@app.route('/', methods=['GET'])
def front_page():
    return render_template('front_page.html')


@app.route('/map/', methods=['POST', 'GET'])
def hello():
    if request.method == 'POST':
        landmark_type = request.form["type"]
        location = request.form["location"]
        address = (request.form["location"]).replace(' ', '+').lower()
        request_url = "https://api.breezometer.com/baqi/?location={0}&key=30783150517b4bf4865869e94c179134".format(address)
        response = requests.get(request_url, verify=False)
        json_response = response.json()

        air_quality = json_response["breezometer_description"]
        air_quality_color = json_response["breezometer_color"]
        air_pollutant = json_response["dominant_pollutant_description"]

        geocode_url = "https://maps.googleapis.com/maps/api/geocode/json?address={0}&key=AIzaSyCLkcGTP4IbCPKTMsiaEgFoIKyDsUjMnZA".format(address)
        map_response = requests.get(geocode_url)
        map_response_json = map_response.json()

        lat = map_response_json["results"][0]["geometry"]["location"]["lat"]
        lng = map_response_json["results"][0]["geometry"]["location"]["lng"]

        return render_template("map_page.html", air_pollutant=air_pollutant, location=location, air_quality=air_quality, air_color=air_quality_color, lat=lat, lng=lng, type=landmark_type)

    if request.method == 'GET':
        new_list = []

        air_quality = request.args.get("air_quality")
        air_color = request.args.get("air_color")
        lat = request.args.get("lat")
        lng = request.args.get("lng")
        landmark_type = request.args.get("landmark_type")

        request_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={0},{1}&radius=2000&type={2}&key=AIzaSyCLkcGTP4IbCPKTMsiaEgFoIKyDsUjMnZA".format(lat, lng, landmark_type)
        response = requests.get(request_url, verify=False)
        json_response = response.json()["results"]

        for object in json_response:
            new_object = {}
            lat = object["geometry"]["location"]["lat"]
            lng = object["geometry"]["location"]["lng"]
            breeze_url = "https://api.breezometer.com/baqi/?lat={0}&lon={1}&key=30783150517b4bf4865869e94c179134".format(lat, lng)
            response = requests.get(breeze_url, verify=False)

            new_object['lat'] = lat
            new_object['lng'] = lng
            new_object['air_quality'] = response.json()['breezometer_description']
            new_list.append(new_object)

        print new_list

        return render_template("map_page.html", air_quality= air_quality, air_color=air_color, lat=lat, lng=lng, list=new_list)


@app.route('/map2/', methods=['POST'])
def bye():
    return request




if __name__ == '__main__':
    app.run(debug=True, port=8000)