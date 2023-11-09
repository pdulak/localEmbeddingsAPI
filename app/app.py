from flask import Flask, jsonify, request, render_template
from sentence_transformers import SentenceTransformer
import json
import requests
from json2html import *

app = Flask(__name__)
qdrant_url = "http://qdrant-api:6333/"
qdrant_collection = "api_collection"


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/search/', methods=['GET'])
def search():
    return render_template("search.html")


@app.route('/initQdrant', methods=['GET'])
def init_qdrant():
    url = f"{qdrant_url}collections/{qdrant_collection}"
    headers = {"Content-Type": "application/json"}
    data = {"vector_size": 768, "distance": "Cosine"}

    response = requests.put(url, headers=headers, data=json.dumps(data))

    return jsonify(str(response)), 200


@app.route('/upsert/', methods=['GET'])
def upsert_get():
    return render_template("upsert.html")


@app.route('/upsert/', methods=['POST'])
def upsert():
    model = SentenceTransformer('sentence-transformers/all-mpnet-base-v2')
    url = f"{qdrant_url}collections/{qdrant_collection}/points"
    headers = {"Content-Type": "application/json"}

    phrase = request.form['phrase']
    embeddings = model.encode(phrase)

    data = {
        "points":[ {
            "id": request.form['ID'],
            "payload": { "phrase": phrase },
            "vector": embeddings.tolist()
        } ]
    }

    upsert_result = requests.put(url, headers=headers, data=json.dumps(data))

    return jsonify({ "term": phrase, "result": upsert_result.json() } ), 200


@app.route('/search/', methods=['POST'])
def search_post():
    model = SentenceTransformer('sentence-transformers/all-mpnet-base-v2')
    embeddings = model.encode(request.form['search_term'])
    url = f"{qdrant_url}collections/{qdrant_collection}/points/search"
    headers = {"Content-Type": "application/json"}
    data = {
        "params": {
            "hnsw_ef": 128,
            "exact": False
        },
        "vector": embeddings.tolist(),
        "limit": 15,
        "with_payload": True
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))

    return jsonify(response.json()["result"]), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0')