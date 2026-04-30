// Export component Header để có thể sử dụng ở các file khác (ví dụ: App.jsx)
// Đây là một React Functional Component
export default function Header() {
  // return: JSX sẽ được render ra giao diện
  return (
    // Thẻ <nav> tạo thanh điều hướng (navigation bar)
    // className là thuộc tính dùng trong React thay cho "class" của HTML
    // navbar navbar-dark bg-dark px-4 là các class của Bootstrap:
    // navbar: định dạng thanh menu
    // navbar-dark + bg-dark: nên màu đen và chữ sáng
    // px-4: padding trái phải
    <nav className="navbar navbar-dark bg-dark px-4">
      {/*
            Thẻ span hiển thị tiêu đề của navbar
            navbar-brand: style cho tên thương hiệu trong Bootstrap
            mb-0: margin-bottom = 0
            hi: kích thước chữ giống heading hi
            text-white: màu chữ trắng
            */}
      <span className="navbar-brand mb-0 h1 text-white">
        {/* Nội dung tiêu đề hiển thị trên thanh header */}
        Data Integration Dashboard
      </span>
    </nav>
  );
}
