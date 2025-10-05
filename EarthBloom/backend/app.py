# backend/app.py
from flask import Flask, render_template, jsonify, request
import json
from utils.bloom_detection import get_bloom_probability
from utils.pollinator_movement import predict_pollinator_flow

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get_bloom", methods=["GET"])
def get_bloom():
    date = request.args.get("date")
    season = request.args.get("season")
    
    with open("data/WildflowerBlooms_AreaOfInterest.json") as f:
        aoi = json.load(f)
    
    bloom_map = get_bloom_probability(aoi, date=date, season=season)
    return jsonify(bloom_map)

@app.route("/get_pollinators", methods=["GET"])
def get_pollinators():
    date = request.args.get("date")
    flow = predict_pollinator_flow(date)
    return jsonify(flow)

if __name__ == "__main__":
    app.run(debug=True)