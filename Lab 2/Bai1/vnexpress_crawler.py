# ==========================================
# CRAWLER LẤY TIN TỪ BÁO VNEXPRESS
# ==========================================

# requests: dùng để gửi yêu cầu HTTP đến website để lấy dữ liệu HTML/XML
import requests

# BeautifulSoup: thư viện phân tích HTML/XML, giúp chúng ta tìm và tách thông tin
from bs4 import BeautifulSoup

def crawl_vnexpress():
    """
    Hàm này sẽ:
    1. Gửi yêu cầu tới RSS của VNExpress
    2. Nhận XML về
    3. Phân tích XML để lấy danh sách bài báo (title, description, link)
    4. Trả về dạng list chứa các dict
    """

    # URL RSS chính thức của VNExpress (dạng XML)
    url = "https://vnexpress.net/rss/tin-moi-nhat.rss"

    # Gửi yêu cầu GET đến server -> server trả về nội dung XML
    response = requests.get(url)

    # Chuyển XML text thành soup để dễ truy xuất
    soup = BeautifulSoup(response.text, "xml")

    # Tìm tất cả các thẻ <item> (mỗi item là một bài báo)
    items = soup.find_all("item")

    articles = []  # List chứa các bài báo

    # Lặp từng bài báo trong RSS
    for item in items:

        # Lấy tiêu đề bài báo trong thẻ <title>
        title = item.title.text

        # Lấy link bài báo trong thẻ <link>
        link = item.link.text

        # Lấy mô tả ngắn trong thẻ <description>
        summary = item.description.text

        # Đưa dữ liệu thành dạng dictionary
        articles.append({
            "title": title,
            "link": link,
            "summary": summary
        })

    # Trả dữ liệu cho API backend
    return articles