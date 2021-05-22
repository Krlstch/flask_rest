import flask
import requests
import ipaddress

app = flask.Flask(__name__, static_folder="templates")

@app.route("/", methods=["GET"])
def start():
    return app.send_static_file("form.html")

@app.route("/answer", methods=["GET"])
def answer():
    # get fields from form
    ip_address = flask.request.args.get("ip")
    
    # check if ip is correct
    try:
        ipaddress.ip_address(ip_address)
    except ValueError:
        return app.send_static_file("error.html")

    # send reqests

    params = {"ip": ip_address}
    # response = requests.get("http://geoplugin.net/json.gp", params=params)
    # data = response.json()
    # country1 = data.get("geoplugin_countryName", "")
    # city1 = data.get("geoplugin_city", "")
    # latitude1 = data.get("geoplugin_latitude", "")
    # longitude1 = data.get("geoplugin_longitude", "")

    # response = requests.get("https://get.geojs.io/v1/ip/geo.json", params=params)
    # data = response.json()[0]
    # country2 = data.get("country", "")
    # city2 = data.get("city", "")
    # latitude2 = data.get("latitude", "")
    # longitude2 = data.get("longitude", "")

    # response = requests.get(f"http://ip-api.com/json/{ip_address}")
    # data = response.json()
    # country3 = data.get("country", "")
    # city3 = data.get("city", "")
    # latitude3 = data.get("lat", "")
    # longitude3 = data.get("lon", "")


    # country1 = "United States"
    # response = requests.get("https://en.wikipedia.org/w/api.php", params=)


    # process


    # generate page
    return flask.render_template("answer.html", text="Hello World")

if __name__ == "__main__":
    app.run(debug=True)