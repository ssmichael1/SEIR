const dbService = require("./covid19_db.js").db
const express = require('express')
var path = require('path');

// First, connect to the database
dbService.connect(err => {
    console.log("Connected")
    if (err) {
        console.log("Error: ", err)
        process.exit(1)
    }
    const app = express()
    const port = 5000

    // Some definitions for static files
    app.get('/', function (req, res) { res.sendFile(path.join(__dirname + '/index.html')) })
    app.get('/sierplot.js', function (req, res) { res.sendFile(path.join(__dirname + '/seirplot.js')) })
    app.get('/favicon.ico', function (req, res) { res.sendFile(path.join(__dirname + "/favicon.ico")) })

    // Custom javascript files
    app.use('/customjs', express.static('customjs'))

    // node.js files
    app.use('/js', express.static('node_modules'))

    /////////////////////////////////////////////////////////////
    // Database Queries
    app.get('/data/state/:statename', function (req, res) {
        dbService.state_data(req.params.statename, result => {
            res.send(result)
        })
    })
    app.get('/data/country/:country', function (req, res) {
        dbService.country_data(req.params.country, result => {
            res.send(result)
        })
    })
    app.get('/data/statelist', function (req, res) {
        dbService.statelist(result => {
            res.send(result)
        })
    })
    app.get('/data/countrylist', function (req, res) {
        dbService.countrylist(result => {
            res.send(result)
        })
    })
    //////////////////////////////////////////////////////////

    app.listen(port, () => console.log(`Example app listening at http://localhost:${port}`))
})