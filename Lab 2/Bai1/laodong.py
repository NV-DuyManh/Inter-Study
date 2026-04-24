import requests
from bs4 import BeautifulSoup

def crawl_laodong():
    url = "https://laodong.vn/rss/thoi-su.rss"
    
    try:
        # Headers giả lập trình duyệt
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        
        response = requests.get(url, headers=headers, timeout=10) # Thêm timeout
        
        # Dùng 'xml' parser. Nếu lỗi thì thử đổi thành 'html.parser'
        soup = BeautifulSoup(response.content, "xml")
        
        items = soup.find_all("item")
        print(f"Lao Động: Tìm thấy {len(items)} bài báo.") # In ra để kiểm tra
        
        articles = []
        
        for item in items:
            title = item.title.text if item.title else "Không tiêu đề"
            link = item.link.text if item.link else "#"
            
            # Xử lý description an toàn hơn
            summary = ""
            if item.description:
                # Xóa các thẻ CDATA nếu còn sót
                summary = item.description.text.replace("<![CDATA[", "").replace("]]>", "").strip()
                # Cắt bớt nếu quá dài
                if len(summary) > 200: 
                    summary = summary[:200] + "..."

            articles.append({
                "title": title,
                "link": link,
                "summary": summary
            })
            
        return articles
        
    except Exception as e:
        print(f"LỖI CRAWL LAO ĐỘNG: {e}") # In lỗi chi tiết ra Terminal
        return []