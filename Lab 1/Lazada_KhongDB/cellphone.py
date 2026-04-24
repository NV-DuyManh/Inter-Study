from flask import Flask, render_template
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import time

app = Flask(__name__)

def get_cellphones_data():
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless") # Tạm thời comment dòng này để bạn thấy trình duyệt chạy và debug dễ hơn
    options.add_argument("--window-size=1920,1080")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    data = []
    try:
        url = "https://cellphones.com.vn/catalogsearch/result?q=điện%20thoại"
        driver.get(url)

        # Cuộn trang từ từ để đảm bảo ảnh load hết (Lazy loading)
        driver.execute_script("window.scrollTo(0, 500);")
        time.sleep(1)
        driver.execute_script("window.scrollTo(0, 1000);")
        time.sleep(3) 

        # Lấy danh sách sản phẩm
        products = driver.find_elements(By.CSS_SELECTOR, ".product-item")
        
        for product in products[:30]:
            try:
                # Lấy tên và giá
                title = product.find_element(By.CSS_SELECTOR, ".product__name").text
                price = product.find_element(By.CSS_SELECTOR, ".product__price--show").text
                link = product.find_element(By.TAG_NAME, "a").get_attribute("href")

                # --- FIX LỖI ẢNH Ở ĐÂY ---
                # Lỗi cũ: find_element(By.CSS_SELECTOR, ".product__image") -> Chỉ lấy được thẻ DIV bao ngoài
                # Sửa lại: Thêm " img" vào selector để lấy thẻ IMG bên trong thẻ DIV đó
                img_element = product.find_element(By.CSS_SELECTOR, ".product__image img")
                
                # Logic lấy src hoặc data-src
                img = img_element.get_attribute("src") # Thử lấy src trước
                
                # Một số web dùng lazyload sẽ để link trong data-src hoặc srcset
                if not img or "base64" in img: 
                    img = img_element.get_attribute("data-src")

                # Nếu vẫn không có thì lấy placeholder
                if not img:
                    img = "https://via.placeholder.com/150"

                data.append({"title": title, "price": price, "img": img, "link": link})
                
            except Exception as e:
                print(f"Lỗi khi lấy từng sản phẩm: {e}")
                continue

    except Exception as e:
        print(f"Lỗi to: {e}")
        
    finally:
        driver.quit()

    return data

@app.route("/")
def home():
    products = get_cellphones_data()
    return render_template("index.html", products=products) # Đảm bảo file index.html hiển thị đúng biến {{ item.img }}

if __name__ == "__main__":
    app.run(debug=True)