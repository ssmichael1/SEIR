import pymongo

# from tabulate import tabulate

_MDB_URL = "mongodb://127.0.0.1:27017"
# _MDB_URL = "mongodb+srv://readonly:readonly@covid-19.hip2i.mongodb.net/covid19"

_client = pymongo.MongoClient(_MDB_URL)
_db = _client.get_database("covid19")
_dbraw = _client.get_database("covid19jhu")
_us = _db.get_collection("us_only")
_global = _db.get_collection("countries_summary")
_pop = _db.get_collection("global")
_uid = _dbraw.get_collection("UID_ISO_FIPS_LookUp_Table")


def state_list():
    return list(_us.distinct("state"))


def country_list():
    clist = list(_global.distinct("country"))
    clist.insert(0, "United States")
    return clist


def country_data(countryname):
    if countryname == "United States":
        countryname = "US"

    population = _uid.find({"Combined_Key": countryname})[0]["Population"]
    pipeline = [
        {"$match": {"country": countryname}},
        {"$sort": {"date": 1}},
        {
            "$project": {
                "_id": 0,
                "date": "$date",
                "count": 1,
                "sum": 1,
                "deaths": "$deaths",
                "confirmed": "$confirmed",
            }
        },
    ]
    return {
        "name": countryname,
        "population": population,
        "series": list(_global.aggregate(pipeline)),
    }


def state_data(statename):
    # A pipeline to aggregate the state data
    pipeline = [
        {"$match": {"state": statename}},
        {
            "$group": {
                "_id": "$date",
                "deaths": {"$sum": "$deaths"},
                "confirmed": {"$sum": "$confirmed"},
            }
        },
        {"$sort": {"_id": 1}},
        {
            "$project": {
                "_id": 0,
                "date": "$_id",
                "count": 1,
                "sum": 1,
                "deaths": "$deaths",
                "confirmed": "$confirmed",
            }
        },
    ]
    # A pipeline to get the population
    pipeline_population = [
        {"$match": {"state": statename}},
        {
            "$group": {
                "_id": "$date",
                "deaths": {"$sum": "$deaths"},
                "confirmed": {"$sum": "$confirmed"},
                "population": {"$sum": "$population"},
            }
        },
        {"$sort": {"_id": -1}},
        {"$limit": 1},
    ]
    population = list(_us.aggregate(pipeline_population))[0]["population"]

    return {
        "name": statename,
        "population": population,
        "series": list(_us.aggregate(pipeline)),
    }


if __name__ == "__main__":
    # print(state_data("Massachusetts"))
    # print(country_data("France"))
    # population = _global.find({"country": ""}).sort("date", 1).limit(1)
    # print(population[0]["population"])
    population = _uid.find({"Combined_Key": "France"})[0]["Population"]
    print(population)

    # pipeline = [
    #    {"$match": {"state": "Texas"}},
    #    {
    #        "$group": {
    #            "_id": "$date",
    #            "deaths": {"$sum": "$deaths"},
    #            "confirmed": {"$sum": "$confirmed"},
    #            "population": {"$sum": "$population"},
    #        }
    #    },
    #    {"$sort": {"_id": -1}},
    #    {"$limit": 1},
    # ]
    # print(list(_us.aggregate(pipeline))[0]["population"])
    # population = (
    #    _global.find({"country": "Australia", "state": []})
    #    .limit(1)
    #    .sort("date", 1)
    # )
    # print(list(population)[0])
