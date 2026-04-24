# =================================================================
# IMPORT CÁC THƯ VIỆN CẦN THIẾT CHO SELENIUM
# =================================================================

from selenium import webdriver
# -> webdriver: Thư viện chính để điều khiển trình duyệt (Chrome, Firefox...)

from selenium.webdriver.common.by import By
# -> By: Dùng để chỉ cách tìm phần tử, VD: By.CSS_SELECTOR, By.ID, By.TAG_NAME

from selenium.webdriver.chrome.service import Service
# -> Service: Cho phép Selenium kết nối với ChromeDriver

from webdriver_manager.chrome import ChromeDriverManager
# -> webdriver_manager: Tự động tải đúng phiên bản ChromeDriver cho máy
# (Không cần tải thủ công)

from selenium.webdriver.chrome.options import Options
# -> Options: Dùng để cấu hình Chrome, ví dụ chạy ẩn (headless), tắt automation, đổi user-agent

import time
# -> time: Dùng để tạm dừng code (sleep) chờ trang web tải xong.

# =================================================================
# HÀM CHÍNH: LẤY DỮ LIỆU SẢN PHẨM TỪ LAZADA
# =================================================================

def get_lazada_products(keyword="điện thoại"):
    """
    - Input: keyword (từ khóa muốn tìm kiếm trên Lazada)
    - Output: trả về danh sách 10 sản phẩm đầu tiên (ở dạng list các dict)
    """
    
    # -------------------------------------------------------------
    # 1. CẤU HÌNH TRÌNH DUYỆT CHROME
    # -------------------------------------------------------------
    options = Options() # tạo object cấu hình Chrome
    
    options.add_argument("--headless=new")
    # -> chạy Chrome ở chế độ ẩn không mở cửa sổ (phù hợp khi làm server)
    
    options.add_argument("--disable-blink-features=AutomationControlled")
    # -> tránh để Lazada phát hiện Selenium đang điều khiển Chrome
    
    options.add_argument("user-agent=Mozilla/5.0")
    # -> đổi User-Agent giống như người dùng thật (ngăn web chặn bot)
    
    # -------------------------------------------------------------
    # 2. KHỞI TẠO CHROME DRIVER
    # -------------------------------------------------------------
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        # -> tự động tải ChromeDriver phù hợp
        
        options=options
        # -> áp dụng cấu hình ở trên
    )
    
    # -------------------------------------------------------------
    # 3. MỞ TRANG TÌM KIẾM LAZADA
    # -------------------------------------------------------------
    url = "https://www.lazada.vn/catalog/?q=điện%20thoại"
    # -> f-string: nhúng keyword vào URL tìm kiếm
    
    driver.get(url)
    # -> mở trang Lazada theo từ khóa
    
    time.sleep(5)
    # -> chờ JavaScript của Lazada tải xong (Lazada load nội dung bằng JS)
    
    # -------------------------------------------------------------
    # 4. CUỘN TRANG ĐỂ LOAD THÊM SẢN PHẨM (lazy-load)
    # -------------------------------------------------------------
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    # -> chạy JavaScript để cuộn xuống cuối trang
    
    time.sleep(3)
    # -> đợi thêm để Lazada tải thêm sản phẩm
    
    # -------------------------------------------------------------
    # 5. TÌM TOÀN BỘ KHỐI SẢN PHẨM
    # -------------------------------------------------------------
    products = driver.find_elements(By.CSS_SELECTOR, ".Bm3ON")
    # -> .Bm3ON là class bao ngoài 1 sản phẩm Lazada
    # -> find_elements: trả về danh sách các phần tử
    
    data = [] # tạo list rỗng để chứa dữ liệu sản phẩm
    
    # -------------------------------------------------------------
    # 6. DUYỆT MỖI SẢN PHẨM (LẤY 10 SẢN PHẨM ĐẦU)
    # -------------------------------------------------------------
    for p in products[:10]: # [:10] nghĩa là lấy 10 phần tử đầu tiên
        
        # -----------------------
        # LẤY TÊN SẢN PHẨM
        # -----------------------
        try:
            title = p.find_element(By.CSS_SELECTOR, ".RfADt").text
            # -> .RfADt là class chứa tên sản phẩm
        except:
            title = "Không rõ tên"
            # -> nếu không tìm thấy class, gán giá trị mặc định
            
        # -----------------------
        # LẤY GIÁ SẢN PHẨM
        # -----------------------
        try:
            price = p.find_element(By.CSS_SELECTOR, ".aBrP0, .oo0xS, ._1cEkb").text
        except:
            price = "Không rõ giá"
        # -----------------------
        # LẤY ẢNH SẢN PHẨM
        # -----------------------
        try:
            img_tag = p.find_element(By.TAG_NAME, "img")
            img = img_tag.get_attribute("src")
            
            if not img or "base64" in img:
                img = img_tag.get_attribute("data-src")
                
            if img and img.startswith("//"):
                img = "https:" + img
        except:
            img = ""
        # -----------------------
        # LẤY LINK SẢN PHẨM
        # -----------------------
        try:
            link = p.find_element(By.TAG_NAME, "a").get_attribute("href")
            # -> thẻ <a> chứa đường link sản phẩm
        except:
            link = "#"
            
        # -----------------------
        # THÊM VÀO DANH SÁCH DATA
        # -----------------------
        data.append({
            "title": title,
            "price": price,
            "img": img,
            "link": link
        })
        
    # -------------------------------------------------------------
    # 7. ĐÓNG TRÌNH DUYỆT VÀ TRẢ KẾT QUẢ
    # -------------------------------------------------------------
    driver.quit()
    # -> tắt Chrome để giải phóng bộ nhớ
    
    return data
    # -> trả về danh sách 10 sản phẩm (dạng list of dict)