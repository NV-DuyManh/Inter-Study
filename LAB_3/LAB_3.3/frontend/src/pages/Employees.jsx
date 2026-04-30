// Import các hook của React
// useState: dùng để lưu dữ liệu trong component
// useEffect: dùng để thực hiện hành động khi component được render (ví dụ gọi API)
import { useEffect, useState } from "react";
// Import Link từ react-router-dom để chuyển trang mà không reload trang
import { Link } from "react-router-dom";

// Component Employees dùng để hiển thị danh sách nhân viên
export default function Employees() {
  // Khai báo state employees để lưu danh sách nhân viên
  // useState([]) nghĩa là giá trị ban đầu là mảng rỗng
  const [employees, setEmployees] = useState([]);

  // Hàm gọi API từ backend Flask để lấy danh sách nhân viên
  const loadEmployees = () => {
    // fetch dùng để gọi HTTP request tới API backend
    fetch("http://localhost:5000/api/employees")
      // Chuyển dữ liệu response thành JSON
      .then((res) => res.json())
      // Sau khi nhận dữ liệu từ backend
      .then((data) => {
        // Lưu dữ liệu vào state employees
        // Khi state thay đổi React sẽ tự động render lại giao diện
        setEmployees(data);
      })
      // Bắt lỗi nếu API bị lỗi
      .catch((err) => console.error("Lỗi tải danh sách:", err));
  };

  // useEffect được gọi khi component được render lần đầu
  // [] nghĩa là chỉ chạy 1 lần khi trang load
  useEffect(() => {
    loadEmployees();
  }, []);

  // Hàm xóa nhân viên
  const deleteEmployee = (id) => {
    // Hiển thị hộp thoại xác nhận trước khi xóa
    if (!window.confirm("Bạn chắc chắn muốn xóa nhân viên này?")) return;

    // Gửi request DELETE tới API Flask
    fetch(`http://localhost:5000/api/employees/${id}`, {
      method: "DELETE",
    })
      // Nhận kết quả trả về từ server
      .then((res) => res.json())
      .then((rs) => {
        // Hiển thị thông báo từ backend
        alert(rs.msg);
        // Nếu xóa thành công thì tải lại danh sách nhân viên
        if (rs.status === "success") loadEmployees();
      });
  };

  // JSX trả về giao diện trang Employees
  return (
    <div>
      {/* Tiêu đề trang */}
      <h3>Employee List</h3>
      {/* Nút chuyển sang trang thêm nhân viên */}
      <Link to="/employees/add" className="btn btn-success mb-3">
        + Add Employee
      </Link>
      {/* Bảng hiển thị danh sách nhân viên */}
      <table className="table table-bordered">
        {/* Phần tiêu đề của bảng */}
        <thead className="table-dark">
          <tr>
            <th>ID</th>
            <th>Full Name</th>
            <th>Department</th>
            <th>Position</th>
            <th style={{ width: "150px" }}>Action</th>
          </tr>
        </thead>
        {/* Phần dữ liệu của bảng */}
        <tbody>
          {/* Dùng map() để lặp qua danh sách employees */}
          {employees.map((emp) => (
            // key giúp React quản lý danh sách hiệu quả
            <tr key={emp.EmployeeID}>
              {/* Hiển thị thông tin từng nhân viên */}
              <td>{emp.EmployeeID}</td>
              <td>{emp.FullName}</td>
              <td>{emp.Department}</td>
              <td>{emp.Position}</td>
              <td>
                {/* Nút Edit để chuyển sang trang chỉnh sửa */}
                <Link
                  className="btn btn-primary btn-sm me-2"
                  to={`/employees/${emp.EmployeeID}`}
                >
                  Edit
                </Link>
                {/* Nút Delete để xóa nhân viên */}
                <button
                  className="btn btn-danger btn-sm"
                  onClick={() => deleteEmployee(emp.EmployeeID)}
                >
                  Delete
                </button>
              </td>
            </tr>
          ))}
          {/* Trường hợp danh sách rỗng */}
          {employees.length === 0 && (
            <tr>
              <td colSpan="5" className="text-center text-muted">
                No data available.
              </td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  );
}
