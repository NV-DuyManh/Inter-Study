from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import config  # Import file config.py

app = Flask(__name__)

# Sử dụng thông tin kết nối từ config.py
app.config["SQLALCHEMY_BINDS"] = {
    "default": config.SQL_SERVER_CONN,  
    "mysql": config.MYSQL_CONN
}

db = SQLAlchemy(app)

# ==========================================
# MÔ HÌNH DỮ LIỆU
# ==========================================

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
    PhongBan = db.Column(db.String(255)) 
    ChucVu = db.Column(db.String(255))   

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

# ==========================================
# CÁC ROUTE CHỨC NĂNG
# ==========================================

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/them-nhan-vien", methods=["GET", "POST"])
def them_nhan_vien():
    if request.method == "POST":
        ho_ten = request.form.get("ho_ten")
        # THÊM BẮT LỖI: Nếu chuỗi rỗng thì gán thành None
        ngay_sinh = request.form.get("ngay_sinh") or None
        gioi_tinh = request.form.get("gioi_tinh")
        dia_chi = request.form.get("dia_chi", "")
        so_dien_thoai = request.form.get("so_dien_thoai")
        email = request.form.get("email")
        # THÊM BẮT LỖI: Nếu chuỗi rỗng thì gán thành None
        ngay_vao_lam = request.form.get("ngay_vao_lam") or None
        phong_ban = request.form.get("phong_ban")
        chuc_vu = request.form.get("chuc_vu")

        lcb = float(request.form.get("luong_co_ban", 0))
        pc = float(request.form.get("phu_cap", 0))
        th = float(request.form.get("thuong", 0))
        kt = float(request.form.get("khau_tru", 0))
        tong_nhan = lcb + pc + th - kt

        nv_sql = HoSoNhanVienSQL(
            HoTen=ho_ten, NgaySinh=ngay_sinh, GioiTinh=gioi_tinh,
            DiaChi=dia_chi, SoDienThoai=so_dien_thoai, Email=email,
            NgayVaoLam=ngay_vao_lam
        )
        db.session.add(nv_sql)
        db.session.commit()

        nv_mysql = HoSoNhanVienMySQL(
            MaNV=nv_sql.MaNV, HoTen=ho_ten, NgaySinh=ngay_sinh, GioiTinh=gioi_tinh,
            SoDienThoai=so_dien_thoai, Email=email, NgayVaoLam=ngay_vao_lam,
            PhongBan=phong_ban, ChucVu=chuc_vu
        )
        db.session.add(nv_mysql)
        
        luong_moi = LuongNhanVien(
            MaNV=nv_sql.MaNV, 
            ThangNam="2026-03-01",
            LuongCoBan=lcb, 
            PhuCap=pc, 
            Thuong=th, 
            KhauTru=kt, 
            LuongThucNhan=tong_nhan
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

@app.route("/in-danh-sach")
def in_danh_sach():
    nhan_viens_sql = HoSoNhanVienSQL.query.all()
    nhan_viens_mysql = HoSoNhanVienMySQL.query.all()
    
    bang_luong = LuongNhanVien.query.all()
    danh_sach_ma_nv_co_luong = [l.MaNV for l in bang_luong] 

    mysql_dict = {nv.MaNV: nv for nv in nhan_viens_mysql}
    merged_data = []

    for nv_sql in nhan_viens_sql:
        co_luong = nv_sql.MaNV in danh_sach_ma_nv_co_luong 

        if nv_sql.MaNV in mysql_dict:
            nv_mysql = mysql_dict[nv_sql.MaNV]
            merged_data.append({
                "MaNV": nv_sql.MaNV,
                "HoTen": nv_sql.HoTen,
                "NgaySinh": nv_sql.NgaySinh,
                "GioiTinh": nv_sql.GioiTinh,
                "DiaChi": nv_sql.DiaChi,
                "SoDienThoai": nv_sql.SoDienThoai,
                "Email": nv_sql.Email,
                "NgayVaoLam": nv_sql.NgayVaoLam,
                "PhongBan": getattr(nv_mysql, "PhongBan", "N/A"), 
                "ChucVu": getattr(nv_mysql, "ChucVu", "N/A"),
                "has_luong": co_luong  
            })
            del mysql_dict[nv_sql.MaNV]  
        else:
            merged_data.append({
                "MaNV": nv_sql.MaNV,
                "HoTen": nv_sql.HoTen,
                "NgaySinh": nv_sql.NgaySinh,
                "GioiTinh": nv_sql.GioiTinh,
                "DiaChi": nv_sql.DiaChi,
                "SoDienThoai": nv_sql.SoDienThoai,
                "Email": nv_sql.Email,
                "NgayVaoLam": nv_sql.NgayVaoLam,
                "PhongBan": "N/A", 
                "ChucVu": "N/A",
                "has_luong": co_luong  
            })
            
    for nv_mysql in mysql_dict.values():
        co_luong = nv_mysql.MaNV in danh_sach_ma_nv_co_luong
        merged_data.append({
            "MaNV": nv_mysql.MaNV,
            "HoTen": nv_mysql.HoTen,
            "NgaySinh": nv_mysql.NgaySinh,
            "GioiTinh": nv_mysql.GioiTinh,
            "DiaChi": getattr(nv_mysql, "DiaChi", "N/A"),
            "SoDienThoai": nv_mysql.SoDienThoai,
            "Email": nv_mysql.Email,
            "NgayVaoLam": nv_mysql.NgayVaoLam,
            "PhongBan": getattr(nv_mysql, "PhongBan", "N/A"),
            "ChucVu": getattr(nv_mysql, "ChucVu", "N/A"),
            "has_luong": co_luong  
        })

    return render_template("in_danh_sach.html", nhan_viens=merged_data)

@app.route("/cap-nhat-nhan-vien/<int:manv>", methods=["GET", "POST"])
def cap_nhat_nhan_vien(manv):
    nhan_vien_sql = HoSoNhanVienSQL.query.get(manv)
    nhan_vien_mysql = HoSoNhanVienMySQL.query.get(manv)

    if not nhan_vien_sql and not nhan_vien_mysql:
        return "Không tìm thấy nhân viên", 404

    if request.method == "POST":
        ho_ten = request.form.get("ho_ten")
        # THÊM BẮT LỖI
        ngay_sinh = request.form.get("ngay_sinh") or None
        gioi_tinh = request.form.get("gioi_tinh")
        dia_chi = request.form.get("dia_chi", "")
        so_dien_thoai = request.form.get("so_dien_thoai")
        email = request.form.get("email")
        # THÊM BẮT LỖI
        ngay_vao_lam = request.form.get("ngay_vao_lam") or None
        phong_ban = request.form.get("phong_ban")
        chuc_vu = request.form.get("chuc_vu")

        if nhan_vien_sql:
            nhan_vien_sql.HoTen = ho_ten
            nhan_vien_sql.NgaySinh = ngay_sinh
            nhan_vien_sql.GioiTinh = gioi_tinh
            nhan_vien_sql.DiaChi = dia_chi
            nhan_vien_sql.SoDienThoai = so_dien_thoai
            nhan_vien_sql.Email = email
            nhan_vien_sql.NgayVaoLam = ngay_vao_lam
            db.session.commit()

        if nhan_vien_mysql:
            nhan_vien_mysql.HoTen = ho_ten
            nhan_vien_mysql.NgaySinh = ngay_sinh
            nhan_vien_mysql.GioiTinh = gioi_tinh
            nhan_vien_mysql.SoDienThoai = so_dien_thoai
            nhan_vien_mysql.Email = email
            nhan_vien_mysql.NgayVaoLam = ngay_vao_lam
            nhan_vien_mysql.PhongBan = phong_ban
            nhan_vien_mysql.ChucVu = chuc_vu
            db.session.commit()

        return redirect(url_for("in_danh_sach")) 

    return render_template("cap_nhat_nhan_vien.html", nv_sql=nhan_vien_sql, nv_mysql=nhan_vien_mysql)

@app.route("/xoa-nhan-vien/<int:manv>", methods=["POST"])
def xoa_nhan_vien(manv):
    luong_nhan_vien = LuongNhanVien.query.filter_by(MaNV=manv).first()
    if luong_nhan_vien:
        db.session.delete(luong_nhan_vien)
        db.session.commit()

    nhan_vien_sql = HoSoNhanVienSQL.query.get(manv)
    if nhan_vien_sql:
        db.session.delete(nhan_vien_sql)
        db.session.commit()

    nhan_vien_mysql = HoSoNhanVienMySQL.query.get(manv)
    if nhan_vien_mysql:
        db.session.delete(nhan_vien_mysql)
        db.session.commit()

    return redirect(url_for("in_danh_sach"))

if __name__ == "__main__":
    app.run(debug=True)