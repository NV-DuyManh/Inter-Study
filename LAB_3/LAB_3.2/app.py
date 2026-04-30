from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import config

app = Flask(__name__)

app.config["SQLALCHEMY_BINDS"] = {
    "default": config.SQL_SERVER_CONN,
    "mysql": config.MYSQL_CONN
}
db = SQLAlchemy(app)

class HoSoNhanVienSQL(db.Model):
    __tablename__ = "HOSONHANVIEN"
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
    MaNV = db.Column(db.Integer, primary_key=True, autoincrement=True)
    HoTen = db.Column(db.String(100), nullable=False)
    NgaySinh = db.Column(db.Date)
    GioiTinh = db.Column(db.String(10))
    SoDienThoai = db.Column(db.String(15))
    Email = db.Column(db.String(100))
    NgayVaoLam = db.Column(db.Date)
    PhongBan = db.Column(db.String(100))
    ChucVu = db.Column(db.String(100))

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

@app.route("/in-danh-sach")
def in_danh_sach():
    nhan_viens_sql = HoSoNhanVienSQL.query.all()
    nhan_viens_mysql = HoSoNhanVienMySQL.query.all()
    mysql_dict = {nv.MaNV: nv for nv in nhan_viens_mysql}
    merged_data = []
    for nv_sql in nhan_viens_sql:
        nv_mysql = mysql_dict.get(nv_sql.MaNV)
        merged_data.append({
            "MaNV": nv_sql.MaNV,
            "HoTen": nv_sql.HoTen,
            "NgaySinh": nv_sql.NgaySinh,
            "GioiTinh": nv_sql.GioiTinh,
            "DiaChi": nv_sql.DiaChi,
            "SoDienThoai": nv_sql.SoDienThoai,
            "Email": nv_sql.Email,
            "NgayVaoLam": nv_sql.NgayVaoLam,
            "PhongBan": getattr(nv_mysql, "PhongBan", "N/A") if nv_mysql else "N/A",
            "ChucVu": getattr(nv_mysql, "ChucVu", "N/A") if nv_mysql else "N/A"
        })
    return render_template("in_danh_sach.html", nhan_viens=merged_data)

@app.route("/cap-nhat-nhan-vien/<int:manv>", methods=["GET", "POST"])
def cap_nhat_nhan_vien(manv):
    nv_sql = HoSoNhanVienSQL.query.get(manv)
    nv_mysql = HoSoNhanVienMySQL.query.get(manv)

    if request.method == "POST":
        if nv_sql:
            nv_sql.HoTen = request.form["ho_ten"]
            nv_sql.NgaySinh = request.form["ngay_sinh"]
            nv_sql.GioiTinh = request.form["gioi_tinh"]
            nv_sql.DiaChi = request.form["dia_chi"]
            nv_sql.SoDienThoai = request.form["so_dien_thoai"]
            nv_sql.Email = request.form["email"]
            nv_sql.NgayVaoLam = request.form["ngay_vao_lam"]

        if nv_mysql:
            nv_mysql.HoTen = request.form["ho_ten"]
            nv_mysql.NgaySinh = request.form["ngay_sinh"]
            nv_mysql.GioiTinh = request.form["gioi_tinh"]
            nv_mysql.SoDienThoai = request.form["so_dien_thoai"]
            nv_mysql.Email = request.form["email"]
            nv_mysql.NgayVaoLam = request.form["ngay_vao_lam"]
            nv_mysql.PhongBan = request.form["phong_ban"]
            nv_mysql.ChucVu = request.form["chuc_vu"]

        db.session.commit()
        return redirect(url_for("in_danh_sach"))

    nv = {
        "HoTen": nv_sql.HoTen if nv_sql else nv_mysql.HoTen,
        "NgaySinh": nv_sql.NgaySinh if nv_sql else nv_mysql.NgaySinh,
        "GioiTinh": nv_sql.GioiTinh if nv_sql else nv_mysql.GioiTinh,
        "DiaChi": nv_sql.DiaChi if nv_sql else "",
        "SoDienThoai": nv_sql.SoDienThoai if nv_sql else nv_mysql.SoDienThoai,
        "Email": nv_sql.Email if nv_sql else nv_mysql.Email,
        "NgayVaoLam": nv_sql.NgayVaoLam if nv_sql else nv_mysql.NgayVaoLam,
        "PhongBan": nv_mysql.PhongBan if nv_mysql else "",
        "ChucVu": nv_mysql.ChucVu if nv_mysql else ""
    }

    return render_template("cap_nhat_nhan_vien.html", nv=nv)

@app.route("/xoa-nhan-vien/<int:manv>", methods=["POST"])
def xoa_nhan_vien(manv):
    if LuongNhanVien.query.filter_by(MaNV=manv).first():
        return "Lỗi: Nhân viên có dữ liệu lương!", 400
    nv_sql = HoSoNhanVienSQL.query.get(manv)
    if nv_sql: db.session.delete(nv_sql)
    nv_mysql = HoSoNhanVienMySQL.query.get(manv)
    if nv_mysql: db.session.delete(nv_mysql)
    db.session.commit()
    return redirect(url_for("in_danh_sach"))

@app.route("/them-nhan-vien", methods=["GET", "POST"])
def them_nhan_vien():
    if request.method == "POST":
        nv_sql = HoSoNhanVienSQL(
            HoTen=request.form["ho_ten"], NgaySinh=request.form["ngay_sinh"],
            GioiTinh=request.form["gioi_tinh"], DiaChi=request.form["dia_chi"],
            SoDienThoai=request.form["so_dien_thoai"], Email=request.form["email"],
            NgayVaoLam=request.form["ngay_vao_lam"]
        )
        db.session.add(nv_sql)
        db.session.commit()
        nv_mysql = HoSoNhanVienMySQL(
            MaNV=nv_sql.MaNV, HoTen=request.form["ho_ten"],
            NgaySinh=request.form["ngay_sinh"], GioiTinh=request.form["gioi_tinh"],
            SoDienThoai=request.form["so_dien_thoai"], Email=request.form["email"],
            NgayVaoLam=request.form["ngay_vao_lam"],
            PhongBan=request.form["phong_ban"], ChucVu=request.form["chuc_vu"]
        )
        db.session.add(nv_mysql)
        db.session.commit()
        return redirect(url_for("index"))
    return render_template("them_nhan_vien.html")

@app.route("/in-bang-luong")
def in_bang_luong():
    nhan_viens = HoSoNhanVienSQL.query.all()
    luong_data = LuongNhanVien.query.all()
    data = []
    for nv in nhan_viens:
        l = next((i for i in luong_data if i.MaNV == nv.MaNV), None)
        if l: data.append((nv, l))
    return render_template("in_bang_luong.html", nhan_viens=data)

if __name__ == "__main__":
    app.run(debug=True)