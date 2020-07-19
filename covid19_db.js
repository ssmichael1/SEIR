const MongoClient = require("mongodb").MongoClient;

//const uri =
//    "mongodb+srv://readonly:readonly@covid-19.hip2i.mongodb.net/covid19";
const uri = "mongodb://127.0.0.1:27017";

const dbService = {
    db: undefined,
    dbraw: undefined,
    uri: "mongodb://127.0.0.1:27017",
    us: undefined,
    global: undefined,
    uid: undefined,
    countrylist: undefined,
    statelist: undefined,
    connect: callback => {
        MongoClient.connect(dbService.uri, { useUnifiedTopology: true }, async function (err, data) {

            if (err) {
                MongoClient.close()
                callback(err);
            }
            console.log("Connected to database");
            dbService.db = data.db("covid19")
            dbService.dbraw = data.db("covid19jhu")
            dbService.us = dbService.db.collection("us_only")
            dbService.global = dbService.db.collection("countries_summary")
            dbService.uid = dbService.dbraw.collection("UID_ISO_FIPS_LookUp_Table")
            // get a list of countires
            /*
            dbService.countrylist = dbService.global.distinct("country", {}, function (err, docs) {
                dbService.countrylist = docs
            })
            dbService.statelist = dbService.us.distinct("state", {}, function (err, docs) {
                dbService.statelist = docs
                console.log(dbService.statelist)
            })
            */
            dbService.countrylist = await dbService.global.distinct("country")
            dbService.statelist = await dbService.us.distinct("state")
            callback(null);
        });
    },
    country_data: function (countryname, callback) {
        if (countryname == "United States")
            countryname = "US"
        retdata = {
            name: countryname,
            population: undefined,
            series: undefined
        }
        dbService.uid.find({ Combined_Key: countryname }).limit(1).toArray(function (err, result) {
            retdata.population = result[0].Population
            pipeline = [
                { $match: { country: countryname } },
                { $sort: { date: 1 } },
                {
                    $project: {
                        _id: 0,
                        date: "$date",
                        count: 1,
                        sum: 1,
                        deaths: "$deaths",
                        confirmed: "$confirmed"
                    }
                }
            ]
            dbService.global.aggregate(pipeline, {}, function (err, data) {
                data.toArray(function (err, series) {
                    retdata.series = series
                    callback(retdata)
                })
            })
        })
    },
    state_data: function (statename, callback) {
        retdata = {
            name: statename,
            population: undefined,
            series: undefined
        }
        pipeline_population = [
            { $match: { state: statename } },
            {
                $group: {
                    _id: "$date",
                    population: { $sum: "$population" }
                }
            },
            { $sort: { _id: -1 } },
            { $limit: 1 },
        ]
        dbService.us.aggregate(pipeline_population, {}, function (err, data) {
            data.toArray(function (err, pseries) {
                retdata.population = pseries[0].population
                pipeline = [
                    { $match: { state: statename } },
                    {
                        $group: {
                            _id: "$date",
                            deaths: { $sum: "$deaths" },
                            confirmed: { $sum: "$confirmed" }
                        }
                    },
                    { $sort: { _id: 1 } },
                    {
                        $project: {
                            _id: 0, date: "$_id", count: 1, sum: 1, deaths: "$deaths", confirmed: "$confirmed",
                        }
                    }
                ]
                dbService.us.aggregate(pipeline, {}, function (err, data) {
                    data.toArray(function (err, series) {
                        retdata.series = series
                        callback(retdata)
                    })
                })
            })
        })

    },
} // end of dbService

module.exports.db = dbService
//export default dbService;

/*
dbService.connect(err => {
    if (err) {
        console.log("Error connecting to database")
    }
    //console.log(dbService.statelist)
    // dbService.country_data("France", result => { console.log(result) })
    dbService.state_data("Massachusetts", result => { console.log(result) })
});
*/
