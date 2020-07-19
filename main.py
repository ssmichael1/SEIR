#! /usr/bin/env python
from flask import Flask, render_template, send_from_directory, jsonify
import json
import covid19_db
from seir import SEIR

seir = SEIR()

# Create the FLASK web server
# keep everything local for simplicity
app = Flask(__name__, static_folder="./", template_folder="./")


# Default route
@app.route("/")
def base_route():
    return render_template("index.html")


@app.route("/seirplot.js")
def seirplot():
    return send_from_directory(".", "seirplot.js")


@app.route("/update_database")
def update_database():
    return "updated"


@app.route("/seir/<string:seirdata>")
def seirfunc(seirdata):
    seir = SEIR()
    jdata = json.loads(seirdata)
    for key, value in jdata.items():
        print(key)
        print(value)
        setattr(seir, key, value)
    data = seir.compute()
    return data


# Serve icon
@app.route("/favicon.ico")
def favicon():
    return send_from_directory(".", "favicon.ico")


@app.route("/customjs/<filename>")
def example(filename):
    return send_from_directory("./customjs", filename)


# Serve data by state
@app.route("/data/state/<statename>")
def statedata(statename):
    return jsonify(covid19_db.state_data(statename))


# Serve data by country
@app.route("/data/country/<countryname>")
def countrydata(countryname):
    return jsonify(covid19_db.country_data(countryname))


# return list of states
@app.route("/data/statelist")
def statelist():
    return jsonify(covid19_db.state_list())


# return list of countries
@app.route("/data/countrylist")
def countrylist():
    return jsonify(covid19_db.country_list())


# Serve stock javascript files from the node_modules directory
# craeated by npm
@app.route("/js/<path:filename>")
def jsdownload(filename):
    return send_from_directory("node_modules", filename)


# Start the app
# Will only be used when running locally in debug mode
if __name__ == "__main__":
    app.run(port=5005, host="0.0.0.0", debug=True)
