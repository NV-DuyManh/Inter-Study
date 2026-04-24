# Import Flask để tạo web server và render_template để hiển thị giao diện HTML
from flask import Flask, render_template

# Import Selenium WebDriver để điều khiển Chrome
from selenium import webdriver
from selenium.webdriver.common.by import By  # Dùng để tìm kiếm phần tử theo CSS, ID, TAG...
from webdriver_manager.chrome import ChromeDriverManager  # Tự động tải và quản lý ChromeDriver

# Khởi tạo ứng dụng Flask
app = Flask(__name__)

def get_lazada_data():
    # Tạo cấu hình cho trình duyệt Chrome
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Chạy Chrome ở chế độ ẩn (không mở cửa sổ)

    # Import Service để kết nối WebDriver với ChromeDriver
    from selenium.webdriver.chrome.service import Service
    # Cài và sử dụng ChromeDriver tự động (không cần tải thủ công)
    service = Service(ChromeDriverManager().install())  # Tạo service cho ChromeDriver
    driver = webdriver.Chrome(service=service, options=options)

    # Mở URL trang tìm kiếm sản phẩm trên Lazada
    url = "https://www.lazada.vn/catalog/?q=điện%20thoại"
    # url = "https://shopee.vn/search?keyword=điện%20thoại"
    driver.get(url)

    # Lấy danh sách các thẻ sản phẩm (mỗi sản phẩm nằm trong một div có class .Bm3ON)
    products = driver.find_elements(By.CSS_SELECTOR, ".Bm3ON")  # Lấy danh sách sản phẩm
    
    # Tạo list để lưu dữ liệu sản phẩm
    data = []
    
    # Duyệt qua 10 sản phẩm đầu tiên
    for product in products[:10]:  # Giới hạn lấy 10 sản phẩm đầu
        try:
            # Lấy tên sản phẩm (nằm trong thẻ có class .RfADt)
            title = product.find_element(By.CSS_SELECTOR, ".RfADt").text
            # Lấy giá sản phẩm (nằm trong thẻ có class .ooOxS)
            price = product.find_element(By.CSS_SELECTOR, ".ooOxS").text
            # Lấy link ảnh (nằm trong thẻ <img>)
            img = product.find_element(By.CSS_SELECTOR, "img").get_attribute("src")
            # Lấy link chi tiết sản phẩm (nằm trong thẻ <a>)
            link = product.find_element(By.TAG_NAME, "a").get_attribute("href")
            # Thêm dữ liệu vào danh sách
            data.append({"title": title, "price": price, "img": img, "link": link})
        except:
            # Nếu bị lỗi (VD: thiếu ảnh, giá, hoặc HTML thay đổi) thì bỏ qua sản phẩm đó
            continue

    # Đóng trình duyệt sau khi lấy xong dữ liệu
    driver.quit()
    # Trả về danh sách sản phẩm
    return data

# Định nghĩa route "/" (trang chủ) cho Flask
@app.route("/")
def home():
    products = get_lazada_data()  # Gọi hàm lấy dữ liệu từ Lazada
    # Trả dữ liệu cho file index.html và hiển thị ra web
    return render_template("index.html", products=products)

# Chạy Flask app nếu file được chạy trực tiếp
if __name__ == "__main__":
    app.run(debug=True)  # debug=True giúp tự động reload khi code thay đổi