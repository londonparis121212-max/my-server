from flask import Flask, request, jsonify
from datetime import datetime
import os
import logging
from functools import wraps

# === НАСТРОЙКА ===
app = Flask(__name__)

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Константы
EXPIRE_TIME = int(datetime(2100, 1, 1).timestamp() * 1000)  # 2100 год
PORT = int(os.environ.get('PORT', 5000))

# === ДЕКОРАТОР ДЛЯ ЛОГИРОВАНИЯ ===
def log_request(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        logger.info(f"📥 {request.method} {request.path}")
        if request.method == 'POST':
            data = request.get_json()
            if data:
                logger.info(f"📦 Данные: key={data.get('key', '')}, deviceId={data.get('deviceId', '')}")
        return f(*args, **kwargs)
    return decorated_function

# === ЭНДПОИНТЫ ===

@app.route('/', methods=['GET'])
@log_request
def index():
    """Корневой эндпоинт"""
    return jsonify({
        "status": "ok",
        "valid": True,
        "message": "VPN Blocker Server Active",
        "version": "2.0"
    })

@app.route('/health', methods=['GET'])
@log_request
def health():
    """Проверка состояния сервера"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "server": "Render"
    })

@app.route('/api/activate-key', methods=['GET', 'POST'])
@log_request
def activate_key():
    """
    Основной эндпоинт для активации ключа
    Поддерживает GET и POST
    """
    
    # Для GET-запросов всегда возвращаем успех
    if request.method == 'GET':
        return jsonify({
            "status": "ok",
            "valid": True,
            "expiresAt": EXPIRE_TIME,
            "method": "GET"
        })
    
    # Для POST-запросов проверяем ключ (если нужно)
    data = request.get_json()
    if data:
        key = data.get('key', '')
        device_id = data.get('deviceId', '')
        
        # Если ключ пустой — всё равно разрешаем (для тестов)
        # В продакшене тут должна быть проверка в БД
        if not key:
            logger.warning("⚠️ Получен пустой ключ, но сервер разрешает")
            return jsonify({
                "status": "warning",
                "valid": True,
                "expiresAt": EXPIRE_TIME,
                "message": "Empty key accepted (debug mode)"
            })
        
        # Любой непустой ключ считается валидным
        return jsonify({
            "status": "ok",
            "valid": True,
            "expiresAt": EXPIRE_TIME,
            "message": f"Key '{key}' activated successfully"
        })
    
    # Если данные не пришли
    return jsonify({
        "status": "error",
        "valid": False,
        "message": "No JSON data provided"
    }), 400

@app.route('/api/activate-key', methods=['GET'])
@log_request
def activate_key_get():
    """GET-запрос для активации (для совместимости)"""
    return jsonify({
        "status": "ok",
        "valid": True,
        "expiresAt": EXPIRE_TIME
    })

# === ОБРАБОТЧИКИ ОШИБОК ===

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "status": "error",
        "message": "Endpoint not found"
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        "status": "error",
        "message": "Internal server error"
    }), 500

# === ЗАПУСК ===
if __name__ == '__main__':
    logger.info(f"🚀 Сервер запущен на порту {PORT}")
    logger.info(f"📅 Дата истечения: {datetime.fromtimestamp(EXPIRE_TIME/1000)}")
    app.run(host='0.0.0.0', port=PORT, debug=False)
