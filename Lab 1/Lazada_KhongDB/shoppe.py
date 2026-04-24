import time
from flask import Flask, render_template
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

app = Flask(__name__)

def get_tiki_data():
    options = webdriver.ChromeOptions()
    # Tắt headless khi đang test để xem trình duyệt chạy thế nào
    # options.add_argument("--headless") 
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    url = "https://tiki.vn/search?q=laptop"
    driver.get(url)

    data = []
    try:
        # 1. Đợi thẻ sản phẩm xuất hiện
        # Tiki dùng class "product-item" cho thẻ bao ngoài cùng
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "product-item")))

        # 2. Lấy danh sách thẻ CHA (thẻ <a> chứa mọi thứ)
        # Thay vì .cWWhxu, hãy dùng .product-item
        products = driver.find_elements(By.CLASS_NAME, "product-item")

        for product in products[:10]:
            try:
                # Tìm Tên: Nằm trong thẻ h3 (dễ tìm hơn class dDeapS)
                title = product.find_element(By.TAG_NAME, "h3").text
                
                # Tìm Giá: Class .price-discount__price là chuẩn
                price = product.find_element(By.CSS_SELECTOR, ".price-discount__price").text
                
                # Tìm Ảnh: Tìm thẻ img bên trong
                # Tiki thường load ảnh dạng webp, lấy src là chuẩn
                img = product.find_element(By.TAG_NAME, "img").get_attribute("src")
                
                # Tìm Link: Chính là thẻ product (vì nó là thẻ <a>)
                link = product.get_attribute("href")
                
                data.append({"title": title, "price": price, "img": img, "link": link})
            except Exception as e:
                # In lỗi ra để biết tại sao bỏ qua
                print(f"Lỗi 1 sp: {e}")
                continue
    finally:
        driver.quit()
    
    return data

@app.route("/")
def home():
    products = get_tiki_data()
    return render_template("index.html", products=products)

if __name__ == "__main__":
    app.run(debug=True, port=5002) # Đổi port khác nếu cần