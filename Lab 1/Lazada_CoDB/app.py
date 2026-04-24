# FILE: app.py
from flask import Flask, render_template
import pymysql

app = Flask(__name__)

def get_products():
    # Kết nối DB để lấy dữ liệu ra
    conn = pymysql.connect(
        host="localhost", 
        user="root", 
        password="Duymanh20092005#", 
        database="shop",
        charset='utf8mb4'
    )
    cursor = conn.cursor()
    cursor.execute("SELECT name, price FROM products")
    data = cursor.fetchall()
    conn.close()
    return data

@app.route("/")
def index():
    products = get_products()
    # Kiểm tra xem có dữ liệu không để báo ra màn hình console
    print(f"Web đã lấy được {len(products)} sản phẩm từ DB.")
    return render_template("index.html", products=products)

if __name__ == "__main__":
    app.run(debug=True)