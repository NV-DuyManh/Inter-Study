# ==========================================
# CRAWLER LẤY TIN TỪ BÁO THANH NIÊN
# ==========================================

import requests
from bs4 import BeautifulSoup

def crawl_thanhnien():
    """
    Hoạt động giống crawl_vnexpress nhưng thay URL RSS.
    """

    # RSS của báo Thanh Niên
    url = "https://thanhnien.vn/rss/home.rss"

    # Gửi yêu cầu GET
    response = requests.get(url)

    # Phân tích XML
    soup = BeautifulSoup(response.text, "xml")

    # Tìm danh sách bài báo
    items = soup.find_all("item")

    articles = []

    # Lặp qua từng bài
    for item in items:
        title = item.title.text
        link = item.link.text
        summary = item.description.text

        articles.append({
            "title": title,
            "link": link,
            "summary": summary
        })

    return articles