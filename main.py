#! /usr/bin/env python
from flask import Flask, render_template, send_from_directory, jsonify

import covid19_rawdata

# Create the FLASK web server
# keep everything local for simplicity
app = Flask(__name__, static_folder="./", template_folder="./")


@app.route("/")
def base_route():
    return render_template("index.html")


# Serve data files from data directory
@app.route("/testdata/<path:filename>")
def datadownload(filename):
    return send_from_directory("data", filename)


# Serve data by state
@app.route("/data/state/<statename>")
def statedata(statename):
    print(statename)
    stateinfo = list(covid19_rawdata.extract_state(statename))
    return jsonify(stateinfo)


# Serve data by country
@app.route("/data/country/<countryname>")
def countrydata(countryname):
    print(countryname)
    countryinfo = list(covid19_rawdata.extract_country(countryname))
    return jsonify(countryinfo)


# Server statelist
@app.route("/data/statelist")
def statelist():
    return jsonify(covid19_rawdata.statelist())


@app.route("/data/countrylist")
def countrylist():
    return jsonify(covid19_rawdata.countrylist())


# Serve stock javascript files from the node_modules directory
# craeated by npm
@app.route("/js/<path:filename>")
def jsdownload(filename):
    return send_from_directory("node_modules", filename)


# Start the app
if __name__ == "__main__":
    app.run(port=5005, host="0.0.0.0", debug=True)
