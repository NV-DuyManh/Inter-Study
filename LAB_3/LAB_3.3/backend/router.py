# 1. IMPORT THƯ VIỆN
# =================
from flask import Blueprint, jsonify, request
# Blueprint: giúp chia cấu trúc API thành từng nhóm riêng. [cite: 579]
# jsonify: dùng để trả dữ liệu JSON về cho Frontend (JavaScript). [cite: 580]
# request: dùng để lấy dữ liệu gửi từ Frontend lên (POST, PUT). [cite: 581]

from config import get_sqlserver_connection, get_mysql_connection
# Import 2 hàm định nghĩa trong file config.py để tạo kết nối đến đúng database tương ứng. [cite: 583, 584]

# 2. TẠO ĐỐI TƯỢNG BLUEPRINT CHỨA TOÀN BỘ API
router = Blueprint("router", __name__) # "router" là tên của Blueprint. [cite: 593, 594]

# -----------------------------------------------------------
# 0. API: LẤY DANH SÁCH PHÒNG BAN (DEPARTMENTS)
# -----------------------------------------------------------
@router.route("/api/departments")
def get_departments():
    sql = get_sqlserver_connection() # Mở kết nối tới database SQL Server (HUMAN) [cite: 599, 601]
    cur = sql.cursor() # cursor dùng để thực thi câu lệnh SQL [cite: 602, 603]
    cur.execute("""
        SELECT DepartmentID, DepartmentName
        FROM Departments
        ORDER BY DepartmentName
    """) # Lấy toàn bộ phòng ban, sắp xếp theo tên [cite: 604, 609]
    
    rows = [
        {"DepartmentID": r[0], "DepartmentName": r[1]}
        for r in cur.fetchall() # fetchall() trả toàn bộ kết quả từ DB. [cite: 610, 612, 613]
    ]
    return jsonify(rows) # Trả dữ liệu JSON về Frontend. [cite: 616, 617]

# -----------------------------------------------------------
# 0. API: LẤY DANH SÁCH CHỨC VỤ (POSITIONS)
# -----------------------------------------------------------
@router.route("/api/positions")
def get_positions():
    sql = get_sqlserver_connection()
    cur = sql.cursor()
    cur.execute("""
        SELECT PositionID, PositionName
        FROM Positions
        ORDER BY PositionName
    """)
    rows = [
        {"PositionID": r[0], "PositionName": r[1]}
        for r in cur.fetchall()
    ]
    return jsonify(rows)

# -----------------------------------------------------------
# 1. API: LẤY DANH SÁCH NHÂN VIÊN (GET EMPLOYEES)
# -----------------------------------------------------------
@router.route("/api/employees")
def get_employees():
    sql = get_sqlserver_connection()
    cur = sql.cursor()
    # Query JOIN 3 bảng để lấy tên phòng ban & chức vụ [cite: 648]
    cur.execute("""
        SELECT e.EmployeeID, e.FullName, d.DepartmentName, p.PositionName
        FROM Employees e
        LEFT JOIN Departments d ON e.DepartmentID = d.DepartmentID
        LEFT JOIN Positions p ON e.PositionID = p.PositionID
        ORDER BY e.EmployeeID
    """)
    rows = [] # list rỗng để bỏ từng nhân viên vào [cite: 656]
    for r in cur.fetchall():
        # Với mỗi dòng dữ liệu trong DB, ta chuyển sang JSON object [cite: 657, 658]
        rows.append({
            "EmployeeID": r[0],
            "FullName": r[1],
            "Department": r[2],
            "Position": r[3]
        })
    return jsonify(rows)

# -----------------------------------------------------------
# 2. API: LẤY CHI TIẾT NHÂN VIÊN THEO ID
# -----------------------------------------------------------
@router.route("/api/employees/<int:emp_id>")
def get_employee_detail(emp_id):
    sql = get_sqlserver_connection()
    cur = sql.cursor()
    cur.execute("""
        SELECT e.EmployeeID, e.FullName, e.Email, e.DateOfBirth, e.Gender, 
               e.[Phone Number], e.HireDate, e.Status, d.DepartmentID, 
               d.DepartmentName, p.PositionID, p.PositionName
        FROM Employees e
        LEFT JOIN Departments d ON e.DepartmentID = d.DepartmentID
        LEFT JOIN Positions p ON e.PositionID = p.PositionID
        WHERE EmployeeID = ?
    """, (emp_id,))
    r = cur.fetchone() # Lấy 1 dòng duy nhất [cite: 698]
    if not r:
        return jsonify({"msg": "Employee not found"}), 404 
    return jsonify({
        "EmployeeID": r[0], "FullName": r[1], "Email": r[2], "DateOfBirth": r[3],
        "Gender": r[4], "PhoneNumber": r[5], "HireDate": r[6], "Status": r[7],
        "DepartmentID": r[8], "DepartmentName": r[9], "PositionID": r[10], "PositionName": r[11]
    })

# -----------------------------------------------------------
# 3. API: THÊM NHÂN VIÊN MỚI (CREATE EMPLOYEE)
# -----------------------------------------------------------
@router.route("/api/employees", methods=["POST"])
def add_employee():
    data = request.get_json() # Lấy JSON mà Frontend gửi qua [cite: 719, 720]
    full_name = data.get("FullName")
    dob = data.get("DateOfBirth")
    gender = data.get("Gender")
    phone = data.get("PhoneNumber")
    email = data.get("Email")
    hire_date = data.get("HireDate")
    dept_id = data.get("DepartmentID") or None
    pos_id = data.get("PositionID") or None
    status = data.get("Status") or "Active"

    sql = get_sqlserver_connection()
    cur = sql.cursor()
    
    # 1. CHECK EMAIL TRÙNG TRONG SQL SERVER [cite: 744]
    cur.execute("SELECT COUNT(*) FROM Employees WHERE Email = ?", (email,))
    if cur.fetchone()[0] > 0:
        return jsonify({"status": "error", "msg": "Email đã tồn tại"}), 400 

    # 2. BẮT ĐẦU TRANSACTION CHO 2 DATABASE [cite: 753]
    my = get_mysql_connection()
    sql.autocommit = False # Buộc SQL Server chờ commit [cite: 756, 758]
    my.start_transaction() # Bắt đầu transaction trong MySQL [cite: 757, 759]

    try:
        # 3. INSERT SQL SERVER VÀ LẤY EMPLOYEEID MỚI [cite: 762]
        cur.execute("""
            INSERT INTO Employees (FullName, DateOfBirth, Gender, [Phone Number], 
                                  Email, HireDate, DepartmentID, PositionID, Status)
            OUTPUT INSERTED.EmployeeID
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (full_name, dob, gender, phone, email, hire_date, dept_id, pos_id, status))
        new_id = int(cur.fetchone()[0]) # Lấy EmployeeID mới tạo [cite: 775, 776]

        # 4. INSERT SANG MYSQL ĐỂ ĐỒNG BỘ PAYROLL [cite: 778]
        my_cur = my.cursor(dictionary=True)
        my_cur.execute("""
            INSERT INTO employees_payroll (EmployeeID, FullName, DepartmentID, PositionID, Status)
            VALUES (%s, %s, %s, %s, %s)
        """, (new_id, full_name, dept_id, pos_id, status))

        # Cả 2 đều thành công -> commit 2 DB [cite: 791]
        sql.commit()
        my.commit()
        return jsonify({"status": "success", "msg": f"Thêm nhân viên thành công (ID = {new_id})"})
    except Exception as e:
        sql.rollback()
        my.rollback()
        return jsonify({"status": "error", "msg": str(e)}), 500

# -----------------------------------------------------------
# 4. API: UPDATE NHÂN VIÊN
# -----------------------------------------------------------
@router.route("/api/employees/<int:emp_id>", methods=["PUT"])
def update_employee(emp_id):
    data = request.get_json()
    full_name = data.get("FullName")
    dob = data.get("DateOfBirth")
    gender = data.get("Gender")
    phone = data.get("PhoneNumber")
    email = data.get("Email")
    hire_date = data.get("HireDate")
    dept_id = data.get("DepartmentID")
    pos_id = data.get("PositionID")
    status = data.get("Status")

    sql = get_sqlserver_connection()
    my = get_mysql_connection()
    sql.autocommit = False
    my.start_transaction()

    try:
        # UPDATE SQL SERVER [cite: 834]
        cur = sql.cursor()
        cur.execute("""
            UPDATE Employees SET FullName=?, DateOfBirth=?, Gender=?, [Phone Number]=?, 
                                Email=?, HireDate=?, DepartmentID=?, PositionID=?, Status=?
            WHERE EmployeeID=?
        """, (full_name, dob, gender, phone, email, hire_date, dept_id, pos_id, status, emp_id))

        # UPDATE MYSQL (PAYROLL) [cite: 863]
        my_cur = my.cursor(dictionary=True)
        my_cur.execute("""
            UPDATE employees_payroll SET FullName=%s, DepartmentID=%s, PositionID=%s, Status=%s
            WHERE EmployeeID=%s
        """, (full_name, dept_id, pos_id, status, emp_id))

        sql.commit()
        my.commit()
        return jsonify({"status": "success", "msg": "Update thành công"})
    except Exception as e:
        sql.rollback()
        my.rollback()
        return jsonify({"status": "error", "msg": str(e)}), 500

# -----------------------------------------------------------
# 5. API: XÓA NHÂN VIÊN
# -----------------------------------------------------------
@router.route("/api/employees/<int:emp_id>", methods=["DELETE"])
def delete_employee(emp_id):
    sql = get_sqlserver_connection()
    my = get_mysql_connection()
    sql.autocommit = False
    my.start_transaction()

    try:
        cur = sql.cursor()
        # CHECK RÀNG BUỘC: NẾU NHÂN VIÊN CÓ DIVIDENDS - KHÔNG XOÁ [cite: 911]
        cur.execute("SELECT COUNT(*) FROM Dividends WHERE EmployeeID=?", (emp_id,))
        if cur.fetchone()[0] > 0:
            return jsonify({"status": "error", "msg": "Không thể xoá nhân viên có Dividends"}), 400

        # XÓA TRONG SQL SERVER [cite: 920]
        cur.execute("DELETE FROM Employees WHERE EmployeeID=?", (emp_id,))

        # XÓA TRONG MYSQL (PAYROLL, ATTENDANCE, SALARIES) [cite: 926]
        my_cur = my.cursor(dictionary=True)
        my_cur.execute("DELETE FROM employees_payroll WHERE EmployeeID=%s", (emp_id,))
        my_cur.execute("DELETE FROM attendance WHERE EmployeeID=%s", (emp_id,))
        my_cur.execute("DELETE FROM salaries WHERE EmployeeID=%s", (emp_id,))

        sql.commit()
        my.commit()
        return jsonify({"status": "success", "msg": "Xoá thành công"})
    except Exception as e:
        sql.rollback()
        my.rollback()
        return jsonify({"status": "error", "msg": str(e)}), 500