from flask import Flask, jsonify, make_response
from flask_cors import CORS
import sqlite3
import os

app = Flask(__name__)
# Разрешаем CORS для всех доменов и заголовков
CORS(app, resources={r"/*": {"origins": "*"}})

@app.after_request
def add_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, ngrok-skip-browser-warning'
    return response

@app.route('/')
def home():
    return "API Toormo работает! Запросы слать на /api/whales"

@app.route('/api/whales', methods=['GET'])
def get_whales():
    try:
        conn = sqlite3.connect('transactions.db')
        conn.row_factory = sqlite3.Row
        rows = conn.execute('SELECT * FROM transactions ORDER BY timestamp DESC LIMIT 50').fetchall()
        conn.close()
        return jsonify([dict(row) for row in rows])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)