import requests
from bs4 import BeautifulSoup
def crawl_vietnamnet():
    """
    Lấy tin mới nhất từ báo VietnamNet
    """
    url = "https://infonet.vietnamnet.vn/rss/doi-song.rss"
    
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "xml")
        
        items = soup.find_all("item")
        articles = []
        
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
    except Exception as e:
        print(f"Lỗi khi crawl VietnamNet: {e}")
        return []