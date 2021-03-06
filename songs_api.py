
from email import message
from urllib import response
from flask import Flask, render_template, request, session, redirect, url_for, flash, jsonify
import pandas as pd

app = Flask(__name__)
data = pd.read_csv("data/songsDataset.csv")

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
        # title_year = title_year.loc[data["year_release"] == int(year)]
        # if int(year) > 0:
        #     title_year = title_year.loc[data["year_release"] == int(year)]
        # if int(yearGT) > 0:
        #     title_year = title_year.loc[data["year_release"] >= int(yearGT)]
    except:
        # return jsonify(
        #     artist = artist,
        #     message = "Bad URI",
        #     output = "Error"
        # )
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
    app.run(debug=True)

# data = pd.read_csv("data/songsDataset.csv")
# a = "Tracy Chapman"
# x = data.loc[data["artists"].str.upper() == a.upper()]
# x = x.loc[data["year_release"] == 1995]
# print(x)