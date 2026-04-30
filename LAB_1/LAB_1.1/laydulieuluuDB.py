from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import pymysql

# Khởi chạy trình duyệt
driver = webdriver.Chrome()
driver.get("https://www.lazada.vn/")
time.sleep(3)

# Tìm kiếm sản phẩm
search_box = driver.find_element(By.NAME, "q")
search_box.send_keys("Laptop Dell")
search_box.send_keys(Keys.RETURN)
time.sleep(10) # Thời gian để bạn gạt Captcha

# Lấy danh sách khung sản phẩm
# (Dùng định danh này là chuẩn nhất, các class khác hay bị đổi)
products = driver.find_elements(By.XPATH, "//div[@data-qa-locator='product-item']")

# Kết nối MySQL
try:
    conn = pymysql.connect(host="localhost", user="root", password="Duymanh20092005#", database="shop", charset='utf8mb4')
    cursor = conn.cursor()
    print("Kết nối MySQL thành công!")

    for product in products[:15]: 
        try:
            # --- SỬA ĐOẠN NÀY ---
            # Cũ: .//a (Nó lấy nhầm link ảnh rỗng)
            # Mới: Tìm thẻ 'a' nào mà có độ dài chữ > 5 ký tự (Tức là có tên)
            product_name = product.find_element(By.XPATH, ".//a[string-length(text()) > 5]").text

            # Lấy giá (Tìm thẻ span có chứa chữ '₫')
            product_price = product.find_element(By.XPATH, ".//span[contains(text(), '₫')]").text

            if product_name and product_price:
                sql = "INSERT INTO products (name, price) VALUES (%s, %s)"
                cursor.execute(sql, (product_name, product_price))
                conn.commit()
                print(f"Đã lưu: {product_name[:20]}... - {product_price}")

        except Exception as e:
            # Lỗi thì bỏ qua, chạy cái tiếp theo
            continue

    conn.close()
except Exception as e:
    print("Lỗi kết nối:", e)

driver.quit()