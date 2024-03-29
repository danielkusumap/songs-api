from flask import Flask, render_template, request, session, redirect, url_for, flash, jsonify
import pandas as pd


app = Flask(__name__)
data = pd.read_csv("data/songsDataset.csv")

@app.route("/")
def index():
    return """
these are examples of using the API</br>
https://songs-api-dnl.herokuapp.com/api?artist=(artist name)</br>
this will return all the songs from the artist and also the Youtube Music link</br></br>

if you need the year of the song, please specify the year and Greater Than Equal (GTE).</br>
https://songs-api-dnl.herokuapp.com/api?artist=(artist name)&year=(year)&yearGTE=(true/false)</br></br>

if yearGTE is true then the API will return all the songs from the artist that has a year release greater than the specific year from the input.</br>
if yearGTE is false then the API will return all the songs from the artist that has a release equal to the specific year from the input.</br>
    """

@app.route("/api", methods=["GET"])
def api():
    artist = request.args.get("artist")
    year = request.args.get("year")
    yearGTE = request.args.get("yearGTE")
    try:
        title_year = data.loc[data["artists"].str.upper() == artist.upper()]
        if yearGTE.upper() == "TRUE":
            title_year = title_year.loc[data["year_release"] >= int(year)]
        elif yearGTE.upper() == "FALSE":
            title_year = title_year.loc[data["year_release"] == int(year)]
    except:
        pass
    finally:
        output = [{"": i,"title": title_year["title"][i], "year_release": str(title_year["year_release"][i]), "ytMusic_URL": str(title_year["ytMusic_URL"][i])} for i in title_year.index]

    if len(output) ==0:
        response = jsonify(
            artist = artist,
            message = "Artist or year not found",
            output = "Error"
        )
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    elif len(output) > 0:
        years_list = sorted(list(set([int(title_year["year_release"][i]) for i in title_year.index])))
        response = jsonify(
            artist = artist,
            message = "Done",
            years_list = years_list,
            output = output
        )
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response

if __name__ == "__main__":
    app.run(threaded=True)
