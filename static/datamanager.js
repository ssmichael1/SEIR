function countrylist(callback) {
    d3.json("static/countries.json")
        .then((data, err) => {
            callback(data.map(a => a.Country).sort())
        })
}

function statelist(callback) {
    d3.json("static/states.json")
        .then((data, err) => {
            callback(data.map(a => a.Name))
        })
}

function state_data(state, callback) {
    d3.json("static/states.json")
        .then((states, err) => {
            cval = states.filter(a => (a.Name == state))
            url = "https://api.covidtracking.com/v1/states/" +
                cval[0].Abbrev.toLowerCase() +
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
                        population: parseInt(cval[0].Population),
                        seirparams: {
                            R0: parseFloat(cval[0].R0),
                            Tinc: parseFloat(cval[0].Tinc),
                            Tinf: parseFloat(cval[0].Tinf),
                            Thos: parseFloat(cval[0].Thos),
                            Tmrec: parseFloat(cval[0].Tmrec),
                            Threc: parseFloat(cval[0].Threc),
                            Tfat: parseFloat(cval[0].Tfat),
                            pMild: parseFloat(cval[0].pMild),
                            pFatal: parseFloat(cval[0].pFatal),
                            Tintervention: parseFloat(cval[0].Tintervention),
                            intervention_duration: parseFloat(cval[0].intervention_duration),
                            R0_intervention: parseFloat(cval[0].R0_intervention),
                            R0_newnormal: parseFloat(cval[0].R0_newnormal),
                            Hc: parseFloat(cval[0].H_c),
                            pfat_increase_nohos: parseFloat(cval[0].pfat_increase_nohos),
                        },
                        seirparamdate: cval[0].Date,
                        series: series
                    }
                    callback(retdata)
                })
        })
}

function country_data(country, callback) {

    d3.json("static/countries.json")
        .then((countries, err) => {
            if (country == 'United States') {
                country = 'United States of America'
            }
            cval = countries.filter(a => a.Country == country)
            d3.json("https://corona-api.com/countries/" +
                String(cval[0].ISO2).toLowerCase())

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