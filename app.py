from flask import Flask, request, jsonify
import os

app = Flask(__name__)
EXPIRE_TIME = 4102444800000  # 2100 год

# --- УНИВЕРСАЛЬНЫЙ ПЕРЕХВАТЧИК (ловит всё, что не обработано ниже) ---
@app.route('/', defaults={'path': ''}, methods=['GET', 'POST', 'PUT', 'DELETE', 'HEAD'])
@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE', 'HEAD'])
def catch_all(path):
    print(f"📥 ПЕРЕХВАЧЕНО: {request.method} /{path}")
    print(f"📥 ТЕЛО: {request.get_data(as_text=True)[:200]}...")
    return jsonify({
        "status": "ok",
        "valid": True,
        "paid": True,
        "expiresAt": EXPIRE_TIME,
        "subscription": {"active": True}
    }), 200

# --- КОНКРЕТНЫЕ ОБРАБОТЧИКИ ДЛЯ ПЛАТЕЖНЫХ ШЛЮЗОВ ---

@app.route('/api/wallet-auth/v1', methods=['POST'])
def wallet_auth():
    print("📥 YooMoney: /api/wallet-auth/v1")
    return jsonify({"status": "ok", "paid": True}), 200

@app.route('/api/frontend/v3', methods=['POST'])
def frontend_v3():
    print("📥 YooKassa: /api/frontend/v3")
    return jsonify({"status": "ok", "paid": True}), 200

@app.route('/api/merchant-profile/v1', methods=['POST'])
def merchant_profile():
    print("📥 YooKassa: /api/merchant-profile/v1")
    return jsonify({"status": "ok", "paid": True}), 200

@app.route('/sdk-api/getIp', methods=['POST', 'GET'])
def get_ip():
    print("📥 safepayonline: /sdk-api/getIp")
    return jsonify({"status": "ok", "ip": "127.0.0.1"}), 200

@app.route('/payment', methods=['POST'])
def payment_gate1():
    print("📥 spendingsplus: /payment")
    return jsonify({"status": "ok", "paid": True}), 200

@app.route('/v2/071c7c55/', methods=['GET', 'POST'])
def mocki():
    print("📥 Mocki.io: /v2/071c7c55/")
    return jsonify({
        "subscription": {
            "active": True,
            "expiresAt": EXPIRE_TIME,
            "status": "active"
        }
    }), 200

# --- ДОПОЛНИТЕЛЬНО: ЕСЛИ ПРИЛОЖЕНИЕ ПРОВЕРЯЕТ ЧТО-ТО ЕЩЁ ---
@app.route('/logs/', methods=['POST'])
def logs():
    print("📥 Получены логи")
    return jsonify({"status": "ok"}), 200

@app.route('/startup.mobile.yandex.net', methods=['GET', 'POST'])
def yandex_startup():
    print("📥 Yandex startup (заглушка)")
    return jsonify({"status": "ok"}), 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
