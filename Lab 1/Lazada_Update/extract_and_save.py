# ============================================================
# HƯỚNG DẪN THỰC HÀNH: LẤY DỮ LIỆU LAZADA: LƯU MYSQL
# ============================================================

from selenium import webdriver
from selenium.webdriver.common.by import By 
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

# Import hàm kết nối MySQL từ file db.py
from db import get_connection

# ============================================================
# HÀM 1: LẤY DỮ LIỆU TỪ LAZADA BẰNG SELENIUM
# ============================================================
def get_lazada_data(keyword="điện thoại"):
    # Tạo cấu hình trình duyệt Chrome
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless=new") # Tắt dòng này để xem trình duyệt chạy

    # Khởi tạo ChromeDriver
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

    # Mở url tìm kiếm Lazada
    url = f"https://www.lazada.vn/catalog/?q={keyword}"
    driver.get(url)

    # Chờ 5 giây để web load hoàn toàn
    time.sleep(5)

    # Tìm tất cả các sản phẩm
    products = driver.find_elements(By.CSS_SELECTOR, ".Bm3ON")
    print(f"👉 TÌM THẤY: {len(products)} SẢN PHẨM")
    
    data = []

    # Lấy 10 sản phẩm đầu tiên
    for p in products[:10]:
        try:
            # 1. Lấy tên sản phẩm (.RfADt)
            try:
                title = p.find_element(By.CSS_SELECTOR, ".RfADt").text
            except:
                title = p.find_element(By.TAG_NAME, "a").text

            # 2. Lấy giá sản phẩm (SỬ DỤNG XPATH ĐỂ TÌM DẤU ₫)
            # Code cũ bị lỗi: price = p.find_element(By.CSS_SELECTOR, ".oo0xS").text (ĐÃ XÓA)
            try:
                price = p.find_element(By.XPATH, ".//span[contains(text(), '₫')]").text
            except:
                # Nếu không thấy dấu đ, tìm chuỗi số
                price = "Liên hệ"

            # 3. Lấy số lượng đã bán (PHỤC HỒI LẠI ĐOẠN NÀY)
            try:
                sold = p.find_element(By.CSS_SELECTOR, ".gAeZC").text
            except:
                sold = "Không rõ"

            # 4. Lấy đánh giá sản phẩm
            try:
                rating = p.find_element(By.CSS_SELECTOR, ".Lh7ru").text
            except:
                rating = "Chưa có"

            # 5. Lấy hình ảnh
            try:
                img = p.find_element(By.TAG_NAME, "img").get_attribute("src")
            except:
                img = ""

            # 6. Lấy link sản phẩm
            try:
                link = p.find_element(By.TAG_NAME, "a").get_attribute("href")
            except:
                link = ""

            # Thêm dữ liệu vào danh sách
            data.append((title, price, sold, rating, img, link))
            print(f"✅ Đã lấy: {title} | Giá: {price}")

        except Exception as e:
            print(f"❌ Lỗi khi lấy sản phẩm: {e}")
            continue

    driver.quit()
    print(f"📊 Tổng số dữ liệu thu được: {len(data)}")
    return data

# ============================================================
# HÀM 2: LƯU DỮ LIỆU XUỐNG MYSQL
# ============================================================
def save_to_mysql(data):
    if not data:
        print("⚠️ Không có dữ liệu để lưu!")
        return

    conn = get_connection()
    cursor = conn.cursor()

    # Lưu ý: Tên bảng là db_shop
    sql = """
    INSERT INTO db_shop (title, price, sold, rating, img, link)
    VALUES (%s, %s, %s, %s, %s, %s)
    """

    try:
        cursor.executemany(sql, data)
        conn.commit()
        print(f"🎉 Đã lưu {len(data)} dòng dữ liệu vào bảng db_shop thành công!")
    except Exception as e:
        print(f"❌ Lỗi khi lưu MySQL: {e}")
    finally:
        conn.close()

# ============================================================
# PHẦN MAIN CHẠY CHƯƠNG TRÌNH
# ============================================================
if __name__ == "__main__":
    data = get_lazada_data()
    save_to_mysql(data)