# ==========================================
# APP.PY – ỨNG DỤNG FLASK CHÍNH (ENTRY POINT)
# ==========================================

# Flask: framework tạo web server
# render_template: dùng để render file HTML trong thư mục templates/
from flask import Flask, render_template

# Import Blueprint API
from routes import news_bp

# Tạo ứng dụng Flask chính
app = Flask(__name__)

# Đăng ký Blueprint vào app
# Mọi API trong news_bp sẽ có prefix /api/news
app.register_blueprint(news_bp, url_prefix="/api/news")

# ----------------- Route trang chủ -----------------
@app.route("/")
def home():
    """
    Khi người dùng truy cập http://127.0.0.1:5000/
    -> Flask sẽ gửi file dashboard.html về trình duyệt
    """
    return render_template("dashboard.html") # Trả giao diện FE

# ----------------- Chạy app -----------------
if __name__ == "__main__":
    # debug=True giúp tự reload khi sửa code
    app.run(debug=True)