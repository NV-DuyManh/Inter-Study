# =================================================================
# APP.PY
# Backend Flask - tích hợp 3 hệ thống vào 1 API duy nhất
# =================================================================

from flask import Flask, jsonify, render_template

# Import 3 hệ thống
from scraper import get_lazada_products
from weather import get_weather
from news import get_news

# Tạo Flask app
app = Flask(__name__)

# =================================================================
# API 1 - Lấy dữ liệu Lazada
# =================================================================
@app.route("/api/lazada")
def api_lazada():
    """
    Khi frontend gọi /api/lazada
    -> Backend gọi scraper.py để lấy dữ liệu
    -> Trả về JSON danh sách sản phẩm
    """
    return jsonify(get_lazada_products())

# =================================================================
# API 2 - Lấy dữ liệu thời tiết
# =================================================================
@app.route("/api/weather")
def api_weather():
    return jsonify(get_weather())

# =================================================================
# API 3 - Lấy dữ liệu tin tức
# =================================================================
@app.route("/api/news")
def api_news():
    return jsonify(get_news())

# =================================================================
# ROUTE TRANG CHỦ - Hiển thị Dashboard
# =================================================================
@app.route("/")
def home():
    return render_template("dashboard.html")  # FE nằm trong templates/

# =================================================================
# CHẠY APP
# =================================================================
if __name__ == "__main__":
    app.run(debug=True)  # debug giúp tự reload khi sửa code