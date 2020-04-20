import pandas
import os
import datetime


def _load_daily_reports():
    basedir = "./COVID-19/"
    world_dir = basedir + "csse_covid_19_data/" + "csse_covid_19_daily_reports"
    files = os.listdir(world_dir)
    daily_reports = {}
    for file in files:
        name, ext = os.path.splitext(file)
        if ext != ".csv":
            continue
        date = datetime.datetime.strptime(name, "%m-%d-%Y").date()
        daily_reports[date] = pandas.read_csv(
            world_dir + os.path.sep + file, header=0
        )
    return daily_reports


def _load_data():
    basedir = "./COVID-19"
    uid_table = pandas.read_csv(
        basedir + "/csse_covid_19_data/UID_ISO_FIPS_LookUp_Table.csv",
        header=0,
        index_col="UID",
    )
    us_deaths = pandas.read_csv(
        basedir
        + "/csse_covid_19_data/csse_covid_19_time_series"
        + "/time_series_covid19_deaths_US.csv",
        header=0,
        index_col="UID",
    )

    return (uid_table, us_deaths)


daily_reports = _load_daily_reports()

# OK, load the data
(uid_table, us_deaths) = _load_data()


def statelist():
    date = datetime.date(2020, 4, 15)
    oneday = daily_reports[date]
    states = oneday.loc[(oneday["Country_Region"] == "US")]
    # Set gets out the unique items
    statelist = set(states["Province_State"])
    statelist = list(statelist)
    statelist.sort()
    # return set as a python list
    return statelist


def countrylist():
    # Arbitrarily pull country list from this file
    date = datetime.date(2020, 4, 15)
    oneday = daily_reports[date]
    countries = set(oneday["Country_Region"])
    countries = list(countries)
    countries.sort()
    countries.insert(0, "United States")
    return countries


def daily_to_dict(data, date):
    active = None
    if "Active" in data:
        active = int(data["Active"].sum())

    return {
        "date": date,
        "confirmed": int(data["Confirmed"].sum()),
        "deaths": int(data["Deaths"].sum()),
        "recovered": int(data["Recovered"].sum()),
        "active": active,
    }


def country_population(countryname):
    if countryname == "United States":
        countryname = "US"
    cdata = uid_table.loc[(uid_table["Combined_Key"] == countryname)]
    population = int(cdata["Population"].values)
    return population


def state_population(statename):
    uid = statename + ", US"
    cdata = uid_table.loc[(uid_table["Combined_Key"] == uid)]
    population = int(cdata["Population"].values)
    return population


def extract_country(countryname):
    if countryname == "United States":
        countryname = "US"
    for date, country in daily_reports.items():
        fieldname = "Country/Region"
        if "Country_Region" in country:
            fieldname = "Country_Region"
        country = country.loc[(country[fieldname] == countryname)]
        yield daily_to_dict(country, date)


def extract_state(statename):
    for date, state in daily_reports.items():
        # There are two possible values for this ... uggghh...
        fieldname = "Province/State"
        if "Province_State" in state:
            fieldname = "Province_State"
        state = state.loc[(state[fieldname] == statename)]
        yield daily_to_dict(state, date)


def countrydata(countryname):
    return {
        "name": countryname,
        "population": country_population(countryname),
        "series": list(extract_country(countryname)),
    }


def statedata(statename):
    return {
        "name": statename,
        "population": state_population(statename),
        "series": list(extract_state(statename)),
    }


if __name__ == "__main__":
    print("testing loading of data")
    d = daily_reports[datetime.date(2020, 4, 15)]
    # d = d.loc[(d["FIPS"] == 840)]
    # print(us_deaths.loc[1003])
    print(country_population("Sweden"))
