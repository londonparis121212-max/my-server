from flask import Flask, request, jsonify
from datetime import datetime
import os

app = Flask(__name__)
EXPIRE_TIME = int(datetime(2100, 1, 1).timestamp() * 1000)

# 📌 НОВЫЙ ОБРАБОТЧИК POST-ЗАПРОСОВ НА КОРЕНЬ "/"
@app.route('/', methods=['POST'])
def index_post():
    print("📥 Получен POST-запрос на корень /")
    return jsonify({
        "status": "ok",
        "valid": True,
        "expiresAt": EXPIRE_TIME
    })

@app.route('/', methods=['GET'])
def index():
    return jsonify({
        "status": "ok",
        "valid": True,
        "message": "VPN Blocker Server Active"
    })

@app.route('/api/activate-key', methods=['GET', 'POST'])
def activate_key():
    if request.method == 'POST':
        data = request.get_json()
        if data:
            print(f"📥 POST на /api/activate-key: key={data.get('key')}")
    
    return jsonify({
        "status": "ok",
        "valid": True,
        "expiresAt": EXPIRE_TIME
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
