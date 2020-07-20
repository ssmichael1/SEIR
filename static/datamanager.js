
function countrylist(callback) {
    d3.json("static/country_codes.json")
        .then((data, err) => {
            callback(data.map(a => a.Name))
        })
}

function statelist(callback) {
    d3.json("static/states.json")
        .then((data, err) => {
            callback(data.map(a => a.name))
        })
}

function state_data(state, callback) {
    d3.json("static/states.json")
        .then((states, err) => {
            cval = states.filter(a => a.name == state)
            url = "https://covidtracking.com/api/v1/states/" +
                cval[0].abbreviation.toLowerCase() +
                "/daily.json"
            d3.json(url)
                .then((cdata, err) => {
                    series = cdata.map(function (a) {
                        year = parseInt(String(a.date).substr(0, 4))
                        month = parseInt(String(a.date).substr(4, 2))
                        day = parseInt(String(a.date).substr(6, 2))
                        return {
                            date: new Date(Date.UTC(year, month - 1, day)),
                            deaths: a.death,
                            confirmed: a.positive
                        }
                    })
                    series = series.sort((a, b) => a.date - b.date)

                    retdata = {
                        name: state,
                        population: cval[0].population,
                        series: series
                    }
                    callback(retdata)
                })
        })
}

function country_data(country, callback) {

    d3.json("static/country_codes.json")
        .then((countries, err) => {
            cval = countries.filter(a => a.Name == country)
            d3.json("https://corona-api.com/countries/" + cval[0].Code)
                .then((cdata, err) => {
                    series = cdata.data.timeline.map(function (a) {
                        return {
                            date: new Date(a.date),
                            deaths: a.deaths,
                            confirmed: a.confirmed
                        }
                    })
                    series = series.sort((a, b) => a.date - b.date)
                    // The most-recent data is for today ... we don't buy it yet...
                    series.pop()

                    retdata = {
                        name: country,
                        population: cdata.data.population,
                        series: series
                    }
                    callback(retdata)
                })
        })
}