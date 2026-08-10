from flask import Flask, request, jsonify
import os
import json
from datetime import datetime

app = Flask(__name__)
EXPIRE_TIME = 4102444800000  # 2100 год

# 📌 ГЛАВНОЕ — перехватываем ВСЕ пути и методы
@app.route('/', defaults={'path': ''}, methods=['GET', 'POST', 'PUT', 'DELETE', 'HEAD'])
@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE', 'HEAD'])
def catch_all(path):
    print(f"📥 ПЕРЕХВАЧЕНО: {request.method} /{path}")
    print(f"📦 Заголовки: {dict(request.headers)}")
    if request.get_json(silent=True):
        print(f"📦 Тело: {request.get_json(silent=True)}")
    
    # Ответ, который говорит "Оплата прошла, доступ есть"
    return jsonify({
        "status": "ok",
        "valid": True,
        "expiresAt": EXPIRE_TIME,
        "payment": {
            "status": "paid",
            "days": 9999
        },
        "message": "Access granted via custom server"
    }), 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
