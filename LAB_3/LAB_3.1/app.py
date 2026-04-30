from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import config

app = Flask(__name__)

app.config["SQLALCHEMY_BINDS"] = {
    "default": config.SQL_SERVER_CONN,
    "mysql": config.MYSQL_CONN
}

db = SQLAlchemy(app)

# --- Mô hình dữ liệu SQL Server ---
class HoSoNhanVienSQL(db.Model):
    __tablename__ = "HoSoNhanVien"
    __bind_key__ = "default"
    MaNV = db.Column(db.Integer, primary_key=True, autoincrement=True)
    HoTen = db.Column(db.String(100), nullable=False)
    NgaySinh = db.Column(db.Date)
    GioiTinh = db.Column(db.String(10))
    DiaChi = db.Column(db.String(255))
    SoDienThoai = db.Column(db.String(15))
    Email = db.Column(db.String(100))
    NgayVaoLam = db.Column(db.Date)

# --- Mô hình dữ liệu MySQL ---
class HoSoNhanVienMySQL(db.Model):
    __tablename__ = "hosonhanvien"
    __bind_key__ = "mysql"
    MaNV = db.Column(db.Integer, primary_key=True) 
    HoTen = db.Column(db.String(100), nullable=False)
    NgaySinh = db.Column(db.Date)
    GioiTinh = db.Column(db.String(10))
    SoDienThoai = db.Column(db.String(15))
    Email = db.Column(db.String(100))
    NgayVaoLam = db.Column(db.Date)
    PhongBan = db.Column(db.String(500))
    ChucVu = db.Column(db.String(500))

class LuongNhanVien(db.Model):
    __tablename__ = "luongnhanvien"
    __bind_key__ = "mysql"
    MaLuong = db.Column(db.Integer, primary_key=True, autoincrement=True)
    MaNV = db.Column(db.Integer, db.ForeignKey("hosonhanvien.MaNV"))
    ThangNam = db.Column(db.Date)
    LuongCoBan = db.Column(db.Float)
    PhuCap = db.Column(db.Float)
    Thuong = db.Column(db.Float)
    KhauTru = db.Column(db.Float)
    LuongThucNhan = db.Column(db.Float)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/them-nhan-vien", methods=["GET", "POST"])
def them_nhan_vien():
    if request.method == "POST":
        # Lấy dữ liệu an toàn bằng .get() để tránh lỗi BadRequestKeyError
        ho_ten = request.form.get("ho_ten")
        ngay_sinh = request.form.get("ngay_sinh")
        gioi_tinh = request.form.get("gioi_tinh")
        dia_chi = request.form.get("dia_chi") # Đây là dòng gây lỗi nếu HTML không có name="dia_chi"
        so_dien_thoai = request.form.get("so_dien_thoai")
        email = request.form.get("email")
        ngay_vao_lam = request.form.get("ngay_vao_lam")
        phong_ban = request.form.get("phong_ban")
        chuc_vu = request.form.get("chuc_vu")

        lcb = float(request.form.get("luong_co_ban", 0))
        pc = float(request.form.get("phu_cap", 0))
        th = float(request.form.get("thuong", 0))
        kt = float(request.form.get("khau_tru", 0))
        tong_nhan = lcb + pc + th - kt

        # 1. SQL Server
        nv_sql = HoSoNhanVienSQL(
            HoTen=ho_ten, NgaySinh=ngay_sinh, GioiTinh=gioi_tinh,
            DiaChi=dia_chi, SoDienThoai=so_dien_thoai, Email=email,
            NgayVaoLam=ngay_vao_lam
        )
        db.session.add(nv_sql)
        db.session.commit()

        # 2. MySQL Hồ sơ
        nv_mysql = HoSoNhanVienMySQL(
            MaNV=nv_sql.MaNV, HoTen=ho_ten, NgaySinh=ngay_sinh, GioiTinh=gioi_tinh,
            SoDienThoai=so_dien_thoai, Email=email, NgayVaoLam=ngay_vao_lam,
            PhongBan=phong_ban, ChucVu=chuc_vu
        )
        db.session.add(nv_mysql)
        
        # 3. MySQL Lương
        luong_moi = LuongNhanVien(
            MaNV=nv_sql.MaNV, ThangNam="2026-03-01",
            LuongCoBan=lcb, PhuCap=pc, Thuong=th, KhauTru=kt, LuongThucNhan=tong_nhan
        )
        db.session.add(luong_moi)
        db.session.commit()

        return redirect(url_for("index"))
    
    return render_template("them_nhan_vien.html")

@app.route("/in-bang-luong")
def in_bang_luong():
    nhan_viens = HoSoNhanVienSQL.query.all()
    bang_luong = LuongNhanVien.query.all()
    data_final = []
    for nv in nhan_viens:
        luong = next((l for l in bang_luong if l.MaNV == nv.MaNV), None)
        if luong is None:
            luong = {'ThangNam': 'Chưa có', 'LuongCoBan': 0, 'PhuCap': 0, 'Thuong': 0, 'KhauTru': 0, 'LuongThucNhan': 0}
        data_final.append((nv, luong))
    return render_template("in_bang_luong.html", nhan_viens=data_final)

if __name__ == "__main__":
    app.run(debug=True)