# =================================================================
# NEWS.PY
# Hệ thống 3: Gọi API Tin tức từ NewsAPI.org
# =================================================================

import requests  # dùng để gửi yêu cầu đến API NewsAPI


def get_news():
    """
    Hàm này sẽ:
    1. Gọi API tin tức
    2. Lấy danh sách bài báo
    3. Trả về 10 bài đầu tiên dạng JSON
    """

    # API key NewsAPI (sinh viên tự đăng ký miễn phí)
    API_KEY = "d2a0760a0ecf4614be439b2fa9be5a29"

    # Gọi tin tức US (có thể đổi thành 'vi' nếu muốn)
    url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={API_KEY}"

    response = requests.get(url)
    data = response.json()

    articles = []

    # Lấy 10 bài đầu
    for a in data["articles"][:10]:
        articles.append({
            "title": a["title"],
            "description": a["description"],
            "url": a["url"]
        })

    return articles