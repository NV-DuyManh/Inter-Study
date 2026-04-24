# ============================================================
# HƯỚNG DẪN THỰC HÀNH: WEB HIỂN THỊ SẢN PHẨM LAZADA TỪ MYSQL
# File: app.py
# Mục tiêu: Xây dựng web server bằng Flask để đọc dữ liệu DB và hiển thị
# ============================================================

# Flask: framework giúp tạo web server bằng Python
from flask import Flask, render_template

# Hàm get_connection() để kết nối MySQL (viết trong file db.py)
from db import get_connection

# ============================================================
# 1) KHỞI TẠO ỨNG DỤNG WEB FLASK
# ============================================================
# Flask(__name__) giúp Flask biết vị trí file đang chạy để quản lý template, static...
app = Flask(__name__)

# ============================================================
# 2) HÀM LẤY DỮ LIỆU TỪ MYSQL
# ============================================================
def get_products_from_db():
    # Mở kết nối đến MySQL thông qua hàm get_connection()
    conn = get_connection()

    # Tạo cursor để gửi câu lệnh SQL
    cursor = conn.cursor()

    # SELECT để lấy toàn bộ dữ liệu trong bảng lazada_products
    cursor.execute("SELECT * FROM db_shop")

    # fetchall() sẽ trả về danh sách tất cả các sản phẩm
    rows = cursor.fetchall()

    # Đóng kết nối DB để tránh lỗi "too many connections"
    conn.close()

    # Trả dữ liệu về cho Flask sử dụng ở phần giao diện
    return rows

# ============================================================
# 3) TẠO ROUTE CHO WEBSITE (TRANG CHỦ)
# ============================================================
# @app.route("/") nghĩa là:
# Khi người dùng truy cập http://localhost:5000/
# -> Chạy hàm home()
@app.route("/")
def home():

    # Gọi hàm đọc dữ liệu MySQL
    products = get_products_from_db()

    # Trả về file HTML index.html trong thư mục templates/
    # Đồng thời gửi danh sách sản phẩm vào biến "products" để HTML hiển thị
    return render_template("index.html", products=products)

# ============================================================
# 4) CHẠY WEB SERVER FLASK
# ============================================================
# Nếu chạy file này trực tiếp (không phải import từ file khác)
if __name__ == "__main__":

    # debug=True giúp Flask tự reload khi thay đổi code
    # và báo lỗi chi tiết nếu có lỗi trong code
    app.run(debug=True)