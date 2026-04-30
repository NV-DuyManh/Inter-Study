// Import component Link từ thư viện react-router-dom
// Link dùng để điều hướng giữa các trang trong React mà không cần reload trang
import { Link } from "react-router-dom";

// Export component Sidebar để sử dụng ở các file khác (ví dụ: App.jsx)
export default function Sidebar() {
  // JSX trả về giao diện của thanh menu bên trái
  return (
    // div ngoài cùng tạo vùng sidebar
    // bg-light: nền màu sáng (Bootstrap)
    // border-end: đường viền bên phải
    // style: đặt chiều rộng sidebar = 220px và chiều cao = toàn màn hình (100vh)
    <div
      className="bg-light border-end"
      style={{ width: "220px", height: "100vh" }}
    >
      {/*
            list-group: component của Bootstrap để tạo danh sách menu
            list-group-flush: bỏ viền ngoài cho danh sách
            */}
      <div className="list-group list-group-flush">
        {/*
                Link điều hướng đến trang "/" (trang danh sách nhân viên)
                to="/": đường dẫn route
                list-group-item: định dạng item trong danh sách Bootstrap
                list-group-item-action: cho phép click giống button
                */}
        <Link to="/" className="list-group-item list-group-item-action">
          Employees
        </Link>
        {/*
                Link điều hướng đến trang thêm nhân viên
                Route: /employees/add
                */}
        <Link
          to="/employees/add"
          className="list-group-item list-group-item-action"
        >
          Add Employee
        </Link>
      </div>
    </div>
  );
}
