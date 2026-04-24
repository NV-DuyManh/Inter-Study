import pyodbc
import mysql.connector

# KẾT NỐI SQL SERVER (HUMAN)
def get_sqlserver_connection():
    try:
        conn = pyodbc.connect(
            "DRIVER={ODBC Driver 17 for SQL Server};"
            "SERVER=(localdb)\\ProjectModels;"  # Sửa lại đúng tên server LocalDB
            "DATABASE=HUMAN_2026_Restore;"           # Database đúng
            "Trusted_Connection=yes;"          # Thường LocalDB dùng Windows Auth
            "timeout=5"
        )
        return conn
    except Exception as e:
        print("Lỗi kết nối SQL Server:", str(e))
        raise

# KẾT NỐI MYSQL (PAYROLL)
def get_mysql_connection():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password=".TranThinh270400",
            database="PAYROLL_2026",
            autocommit=False # REQUIRED cho 2-phase-commit
        )
        return conn
    except Exception as e:
        print("Lỗi kết nối MySQL:", str(e))
        raise