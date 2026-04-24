# =========================================================
# ROUTES.PY – CHỨA CÁC API BACKEND TRẢ DỮ LIỆU CHO FRONTEND
# =========================================================

# Blueprint: cho phép tạo nhóm API riêng, giúp tổ chức backend thành module
from flask import Blueprint, jsonify

# Import 2 crawler để gọi khi API được gọi
from vnexpress_crawler import crawl_vnexpress
from thanhnien_crawler import crawl_thanhnien
from tuoitre import crawl_tuoitre
from laodong import crawl_laodong
from vietnamnet import crawl_vietnamnet
# Tạo Blueprint tên "news"
# url_prefix sẽ được cấu hình trong app.py
news_bp = Blueprint("news", __name__)

# --------- API 1: Lấy tin VNExpress ---------
@news_bp.route("/vnexpress")
def api_vnexpress():
    """
    Khi frontend gọi /api/news/vnexpress:
    1. Hàm này chạy
    2. Gọi crawler để lấy dữ liệu
    3. Trả về JSON
    """

    articles = crawl_vnexpress()  # Lấy bài báo
    return jsonify(articles)      # Chuyển thành JSON gửi về FE

# --------- API 2: Lấy tin Thanh Niên ---------
@news_bp.route("/thanhnien")
def api_thanhnien():
    articles = crawl_thanhnien()  # Tương tự trên
    return jsonify(articles)
@news_bp.route("/tuoitre")
def api_tuoitre():
    articles = crawl_tuoitre()
    return jsonify(articles)

@news_bp.route("/vietnamnet")
def api_vietnamnet():
    articles = crawl_vietnamnet()
    return jsonify(articles)

@news_bp.route("/laodong")
def api_laodong():
    articles = crawl_laodong()
    return jsonify(articles)