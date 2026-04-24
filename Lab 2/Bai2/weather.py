# =================================================================
# WEATHER.PY
# Hệ thống 2: Gọi API Thời tiết từ OpenWeatherMap
# =================================================================

import requests  # requests để gọi API qua HTTP


def get_weather(city="Da Nang"):
    """
    Hàm này sẽ:
    1. Gọi API của OpenWeatherMap
    2. Nhận dữ liệu thời tiết dạng JSON
    3. Trả về thông tin: nhiệt độ, độ ẩm, mô tả thời tiết
    """

    # API key của OpenWeatherMap (sinh viên phải đăng ký miễn phí)
    API_KEY = "a005944aeb3ac27ddd1a32e65e7618f4"

    # URL gọi API, đơn vị nhiệt độ (units=metric -> độ C)
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

    # Gửi GET request đến API
    response = requests.get(url)

    # Parse JSON thành dictionary Python
    data = response.json()

    # Trả về dữ liệu cần thiết
    return {
        "city": city,
        "temp": data["main"]["temp"],
        "humidity": data["main"]["humidity"],
        "description": data["weather"][0]["description"]
    }