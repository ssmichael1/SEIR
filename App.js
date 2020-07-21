const express = require('express')
var path = require('path');


const app = express()
const port = 5000

// Some definitions for static files
app.get('/', function (req, res) { res.sendFile(path.join(__dirname + '/index.html')) })
app.get('/favicon.ico', function (req, res) { res.sendFile(path.join(__dirname + "/favicon.ico")) })

// Custom javascript files
app.use('/customjs', express.static('customjs'))
app.use('/static', express.static('static'))
app.use('/data', express.static('data'))

//////////////////////////////////////////////////////////
app.listen(port, () => console.log(`Example app listening at http://localhost:${port}`))