import requests
from bs4 import BeautifulSoup
def crawl_tuoitre():
    """
    Lấy tin mới nhất từ báo Tuổi Trẻ
    """
    url = "https://tuoitre.vn/rss/tin-moi-nhat.rss"
    
    try:
        response = requests.get(url)
        # Báo Tuổi Trẻ trả về XML chuẩn
        soup = BeautifulSoup(response.text, "xml")
        
        items = soup.find_all("item")
        articles = []
        
        for item in items:
            title = item.title.text
            link = item.link.text
            # Tuổi trẻ dùng CDATA trong description, soup.text vẫn lấy được tốt
            summary = item.description.text
            
            articles.append({
                "title": title,
                "link": link,
                "summary": summary
            })
            
        return articles
    except Exception as e:
        print(f"Lỗi khi crawl Tuổi Trẻ: {e}")
        return []