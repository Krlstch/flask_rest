import flask
import requests
import ipaddress
import numpy as np

app = flask.Flask(__name__, static_folder="templates")

@app.route("/", methods=["GET"])
def start():
    return app.send_static_file("form.html")

@app.route("/answer", methods=["GET"])
def answer():
    ## get fields from form
    ip_address = flask.request.args.get("ip")
    
    ## check if ip is correct
    try:
        ipaddress.ip_address(ip_address)
    except ValueError:
        return app.send_static_file("error.html")

    ## send reqests

    params = {"ip": ip_address}
    response = requests.get("http://geoplugin.net/json.gp", params=params)
    data = response.json()
    country1 = data.get("geoplugin_countryName", "")
    city1 = data.get("geoplugin_city", "")
    latitude1 = data.get("geoplugin_latitude", "")
    longitude1 = data.get("geoplugin_longitude", "")

    response = requests.get("https://get.geojs.io/v1/ip/geo.json", params=params)
    data = response.json()[0]
    country2 = data.get("country", "")
    city2 = data.get("city", "")
    latitude2 = data.get("latitude", "")
    longitude2 = data.get("longitude", "")

    response = requests.get(f"http://ip-api.com/json/{ip_address}")
    data = response.json()
    country3 = data.get("country", "")
    city3 = data.get("city", "")
    latitude3 = data.get("lat", "")
    longitude3 = data.get("lon", "")

    country = max(country1, country2, country3, key=lambda x: len(x))

    if country != "":
        response = requests.get(f"https://restcountries.eu/rest/v2/name/{country}")
        data = response.json()[-1]
        name = data.get("name", "")
        area = data.get("area", "")
        population = data.get("population", "")
        capital = data.get("capital", "")
    else:
        name = ""
        area = ""
        population = ""
        capital = ""

    ## process

    #check if all apis returned same country
    same_country = "Same" if country1 == country2 == country3 else "Different"
    
    #check if all apis returned same city
    same_city = "Same" if city1 == city2 == city3 else "Different"

    # Latitude
    latitude_floats = []
    for latitude in (latitude1, latitude2, latitude3):
        if latitude != "":
            latitude_floats.append(float(latitude))
    if latitude_floats:
        latitude_avg = np.average(latitude_floats)
        latitude_std = np.average(latitude_floats)
    else:
        latitude_avg = 0
        latitude_std = 0

    # longitude
    longitude_floats = []
    for longitude in (longitude1, longitude2, longitude3):
        if longitude != "":
            longitude_floats.append(float(longitude))
    if longitude_floats:
        longitude_avg = np.average(longitude_floats)
        longitude_std = np.average(longitude_floats)
    else:
        longitude_avg = 0
        longitude_std = 0


    # generate page
    return flask.render_template("answer.html", country1=country1, city1=city1, latitude1=latitude1, longitude1=longitude1,
                                                country2=country2, city2=city2, latitude2=latitude2, longitude2=longitude2,
                                                name=name, area=area, population=population, capital=capital,
                                                same_country=same_country, same_city=same_city, 
                                                latitude_avg=latitude_avg, latitude_std=latitude_std,
                                                longitude_avg=longitude_avg, longitude_std=longitude_std)

if __name__ == "__main__":
    app.run(debug=True)