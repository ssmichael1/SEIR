function countrylist(callback) {
    d3.json("static/countries.json")
        .then((data, err) => {
            callback(data.map(a => a.Name).sort())
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
                        population: cval[0].Population,
                        seirparams: {
                            R0: cval[0].R0,
                            Tinc: cval[0].Tinc,
                            Tinf: cval[0].Tinf,
                            Thos: cval[0].Thos,
                            Tmrec: cval[0].Tmrec,
                            Threc: cval[0].Threc,
                            Tfat: cval[0].Tfat,
                            pMild: cval[0].pMild,
                            pFatal: cval[0].pFatal,
                            Tintervention: cval[0].Tintervention,
                            intervention_duration: cval[0].intervention_duration,
                            R0_intervention: cval[0].R0_intervention,
                            R0_newnormal: cval[0].R0_newnormal,
                            Hc: cval[0].H_c,
                            pfat_increase_nohos: cval[0].pfat_increase_nohos,
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
            cval = countries.filter(a => a.Name == country)
            d3.json("https://covidapi.info/api/v1/country/" +
                String(cval[0].ISO3))

                .then((cdata, err) => {
                    series = Object.keys(cdata.result).map(function (key) {
                        return {
                            date: new Date(key),
                            deaths: cdata.result[key].deaths,
                            confirmed: cdata.result[key].confirmed
                        }
                    })
                    series = series.sort((a, b) => a.date - b.date)
                    // The most-recent data is for today ... we don't buy it yet...
                    series.pop()

                    retdata = {
                        name: country,
                        population: cval[0].Population,
                        seirparams: {
                            R0: cval[0].R0,
                            Tinc: cval[0].Tinc,
                            Tinf: cval[0].Tinf,
                            Thos: cval[0].Thos,
                            Tmrec: cval[0].Tmrec,
                            Threc: cval[0].Threc,
                            Tfat: cval[0].Tfat,
                            pMild: cval[0].pMild,
                            pFatal: cval[0].pFatal,
                            Tintervention: cval[0].Tintervention,
                            intervention_duration: cval[0].intervention_duration,
                            R0_intervention: cval[0].R0_intervention,
                            R0_newnormal: cval[0].R0_newnormal,
                            Hc: cval[0].H_c,
                            pfat_increase_nohos: cval[0].pfat_increase_nohos,
                        },
                        seirparamdate: cval[0].Date,
                        series: series
                    }
                    callback(retdata)
                })
        })
}