from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS

from database import (
    init_db,
    get_stats,
    get_cleanups,
    get_spots
)

app = Flask(__name__)
CORS(app)

init_db()


@app.route('/')
def home():
    return send_from_directory('.', 'index.html')


@app.route('/api/stats')
def stats():
    return jsonify(get_stats())


@app.route('/api/cleanups')
def cleanups():
    return jsonify(get_cleanups())


@app.route('/api/spots')
def spots():
    return jsonify(get_spots())


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)