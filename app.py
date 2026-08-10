from flask import Flask, request, jsonify
import os

app = Flask(__name__)
EXPIRE_TIME = 4102444800000  # 2100 год

# Универсальный перехватчик (на всё, что не обработано ниже)
@app.route('/', defaults={'path': ''}, methods=['GET', 'POST', 'PUT', 'DELETE', 'HEAD'])
@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE', 'HEAD'])
def catch_all(path):
    print(f"📥 ПЕРЕХВАЧЕНО: {request.method} /{path}")
    if request.get_json(silent=True):
        print(f"📦 Тело: {request.get_json(silent=True)}")
    
    return jsonify({
        "status": "ok",
        "valid": True,
        "paid": True,
        "expiresAt": EXPIRE_TIME
    }), 200

# Конкретные обработчики для платёжных запросов
@app.route('/api/wallet-auth/v1', methods=['POST'])
def wallet_auth():
    print("📥 YooMoney wallet-auth")
    return jsonify({"status": "ok", "paid": True}), 200

@app.route('/api/frontend/v3', methods=['POST'])
def frontend_v3():
    print("📥 YooKassa frontend")
    return jsonify({"status": "ok", "paid": True}), 200

@app.route('/api/merchant-profile/v1', methods=['POST'])
def merchant_profile():
    print("📥 YooKassa merchant-profile")
    return jsonify({"status": "ok", "paid": True}), 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
