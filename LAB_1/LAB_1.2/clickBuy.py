# 0.Cài đặt thư viện: pip install selenium flask webdriver-manager

# 1.Import thư viện
#-flask tạo WebSever, render_template hiển thị GUI HTML(data to HTML)
#-selenium webdriver: công cụ crawl data
#-dùng để tìm kiếm phần tử CSS
#-tải và quản lý ChromeDriver
from flask import Flask, render_template 
from selenium import webdriver
from selenium.webdriver.common.by import By 
from webdriver_manager.chrome import ChromeDriverManager 

# 2.khởi tạo ứng dụng web flask
app = Flask(__name__) 


# 3.Tạo hàm
def get_shopee_data(): #khai báo hàm trong python

# 4. Thiết lập Chrome
    #tạo cấu hình cho trình duyệt chrome
    options = webdriver.ChromeOptions();
    #chạy Chrome ở chế độ ẩn
    options.add_argument("__headless")  

# 5.Chạy Chrome Driver
    #import service để kết nối webdriver với ChromeDriver
    from selenium.webdriver.chrome.service import Service
    #Cài và sử dụng chromeDriver(tự động tải)
    service = Service(ChromeDriverManager().install()) #tạo service cho chromeDriver
    driver = webdriver.Chrome(service=service, options=options) #Driver: robot trình duyệt selenium

# 6. Mở web Shopee
    url = "https://clickbuy.com.vn/tim-kiem?key=%C4%91i%E1%BB%87n-tho%E1%BA%A1i"
    driver.get(url)

# 7. Lấy danh sách sản phẩm
    #.col-xs-2-4 shopee-search-item-result__item: class khung sản phẩm
    products = driver.find_elements(By.CSS_SELECTOR, ".list-products__item ")

# 8. Tạo List(mảng) để lưu dữ sản phẩm
    data = [] #data là 1 list lưu nhiều sản phẩm

# 9.Lặp qua từng sản phẩm
    for product in products[:10]: #lấy 10 sản phẩm đầu tiên

# 10.Lấy từng trường thông tin
        try:
        #lấy tên sản phẩm()
            title = product.find_element(By.CSS_SELECTOR,".title_name").text
            price = product.find_element(By.CSS_SELECTOR,".new-price").text
            img = product.find_element(By.CSS_SELECTOR,".lazyload").get_attribute("src")
            link = product.find_element(By.TAG_NAME,"a").get_attribute("href")

# 11. Thêm vào danh sách dữ liệu
            data.append({"title":title,"price":price,"img":img,"link":link})
        except:
        #Nếu bị lỗi thì bỏ qua sản phẩm đó
            continue
    driver.quit()

# 12. Trả kết quả về FLask
    return data

# 13. Tạo route chp trang web
# Định nghĩa route cho trang web
@app.route("/")
def home():
    products = get_shopee_data()

    return render_template("index.html", products= products)


# 14. Chạy sever: Chạy Flask app nếu file được chạy trực tiếp
if __name__ == "__main__":
    app.run(debug=True)
