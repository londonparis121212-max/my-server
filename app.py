from flask import Flask, request, jsonify
from datetime import datetime
import os

app = Flask(__name__)
EXPIRE_TIME = int(datetime(2100, 1, 1).timestamp() * 1000)

@app.route('/', methods=['GET'])
def index():
    return jsonify({
        "status": "ok",
        "valid": True,
        "message": "VPN Blocker Server Active"
    })

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy"})

@app.route('/api/activate-key', methods=['GET', 'POST'])
def activate_key():
    # Логируем запрос (для отладки)
    if request.method == 'POST':
        data = request.get_json()
        if data:
            print(f"POST: key={data.get('key')}, deviceId={data.get('deviceId')}")
    
    # ✅ ПРАВИЛЬНЫЙ ОТВЕТ
    return jsonify({
        "status": "ok",
        "valid": True,
        "expiresAt": EXPIRE_TIME
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
