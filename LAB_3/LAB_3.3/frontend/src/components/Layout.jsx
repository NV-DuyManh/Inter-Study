// Import component Header từ file Header.jsx
// Header dùng để hiển thị thanh tiêu đề ở phía trên của website
import Header from "./Header";

// Import component Sidebar từ file Sidebar.jsx
// Sidebar là menu điều hướng ở bên trái
import Sidebar from "./Sidebar";

// Export component Layout để sử dụng trong các trang khác
// { children } là props đặc biệt của React dùng để hiển thị nội dung con bên trong Layout
export default function Layout({ children }) {
  // JSX trả về cấu trúc bố cục chung của toàn bộ ứng dụng
  return (
    // div bao ngoài cùng của layout
    <div>
      {/* Hiển thị thanh Header ở phía trên */}
      <Header />
      {/*
            div chứa Sidebar và nội dung chính
            display: flex giúp bố trí các phần tử theo chiều ngang
            */}
      <div style={{ display: "flex" }}>
        {/* Hiển thị menu bên trái */}
        <Sidebar />
        {/*
                main là vùng nội dung chính của trang
                flexGrow: 1 giúp phần này chiếm toàn bộ không gian còn lại
                p-4 là class Bootstrap tạo padding
                */}
        <main style={{ flexGrow: 1 }} className="p-4">
          {/*
                    children là nội dung của từng trang sẽ được render tại đây
                    Ví dụ: Employees page, Add Employee page
                    */}
          {children}
        </main>
      </div>
    </div>
  );
}
