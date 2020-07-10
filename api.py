from flask import Flask, jsonify
from flask_cors import CORS, cross_origin

import json
import requests

app = Flask(__name__)
cors = CORS(app)
app.config["DEBUG"] = True

conf = json.loads(open("config.json", "r").read())

def get_username(summoner_id):
    r = requests.get("https://na1.api.riotgames.com/lol/summoner/v4/summoners/" + str(summoner_id), headers={"X-Riot-Token": conf["API_KEY"]})
    return json.loads(r.text)["name"]

def get_summoner_id(username):
    r = requests.get("https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/" + str(username), headers={"X-Riot-Token": conf["API_KEY"]})
    return json.loads(r.text)["id"]

def get_clash_team_id(summoner_id):
    r = requests.get("https://na1.api.riotgames.com/lol/clash/v1/players/by-summoner/" + str(summoner_id), headers={"X-Riot-Token": conf["API_KEY"]})
    return json.loads(r.text[1:-1])["teamId"]

def get_clash_team(team_id):
    r = requests.get("https://na1.api.riotgames.com/lol/clash/v1/teams/" + str(team_id), headers={"X-Riot-Token": conf["API_KEY"]})
    return json.loads(r.text)


@app.route("/api/getuserinfo/<string:username>", methods=["GET"])
@cross_origin()
def get_team_data(username):
    s_id = get_summoner_id(username)
    team_id = get_clash_team_id(s_id)
    clash_team = get_clash_team(team_id)

    for player in clash_team["players"]:
        player["name"] = get_username(player["summonerId"])

    return clash_team

if __name__ == "__main__":
    app.run(host="0.0.0.0")
