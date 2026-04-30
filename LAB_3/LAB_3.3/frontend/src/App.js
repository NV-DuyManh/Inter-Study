// Import các component cần thiết từ thư viện react-router-dom
// BrowserRouter: quản lý routing của ứng dụng React
// Routes: chứa danh sách các route
// Route: định nghĩa từng đường dẫn và component tương ứng
import { BrowserRouter, Routes, Route } from "react-router-dom";

// Import Layout để tạo bố cục chung (Header + Sidebar + Main Content)
import Layout from "./components/Layout";

// Import các trang (pages) của ứng dụng
// Employees: trang hiển thị danh sách nhân viên
import Employees from "./pages/Employees";

// EmployeeAdd: trang thêm nhân viên mới
import EmployeeAdd from "./pages/EmployeeAdd";

// EmployeeEdit: trang chỉnh sửa thông tin nhân viên
import EmployeeEdit from "./pages/EmployeeEdit";

// Component chính của toàn bộ ứng dụng React
function App() {
  // JSX trả về cấu trúc routing của ứng dụng
  return (
    // BrowserRouter bao toàn bộ ứng dụng để kích hoạt hệ thống routing
    <BrowserRouter>
      {/* Layout chứa Header + Sidebar + vùng nội dung */}
      <Layout>
        {/* Routes chứa tất cả các đường dẫn của ứng dụng */}
        <Routes>
          {/*
                    Route trang chủ
                    path="/" nghĩa là khi truy cập đường dẫn gốc
                    element={<Employees />} nghĩa là render component Employees
                    */}
          <Route path="/" element={<Employees />} />

          {/*
                    Route thêm nhân viên
                    Khi truy cập /employees/add sẽ hiển thị trang EmployeeAdd
                    */}
          <Route path="/employees/add" element={<EmployeeAdd />} />

          {/*
                    Route chỉnh sửa nhân viên
                    :id là tham số động (dynamic parameter)
                    Ví dụ: /employees/5
                    Trang EmployeeEdit sẽ nhận id để load dữ liệu nhân viên tương ứng
                    */}
          <Route path="/employees/:id" element={<EmployeeEdit />} />
        </Routes>
      </Layout>
    </BrowserRouter>
  );
}

// Export App để sử dụng trong file index.js
export default App;
