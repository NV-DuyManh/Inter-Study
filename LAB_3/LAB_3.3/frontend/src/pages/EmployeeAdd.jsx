// Import các React hooks
import { useEffect, useState } from "react";
// useNavigate dùng để chuyển trang bằng code
import { useNavigate } from "react-router-dom";

// Component dùng để thêm nhân viên mới
export default function EmployeeAdd() {
  // nav dùng để điều hướng trang
  const nav = useNavigate();

  // STATE lưu dữ liệu của form
  const [form, setForm] = useState({
    FullName: "",
    DateOfBirth: "",
    Gender: "",
    PhoneNumber: "",
    Email: "",
    HireDate: "",
    DepartmentID: "",
    PositionID: "",
    Status: "Active", // giá trị mặc định
  });

  // STATE lưu dữ liệu cho dropdown
  const [departments, setDepartments] = useState([]);
  const [positions, setPositions] = useState([]);

  // Hàm xử lý khi người dùng thay đổi dữ liệu trong form
  const handleChange = (e) => {
    // Cập nhật state form
    setForm({
      ...form, // giữ nguyên các field cũ
      [e.target.id]: e.target.value, // cập nhật field đang thay đổi
    });
  };

  // Hàm load dữ liệu cho dropdown (department và position)
  const loadDropdowns = () => {
    fetch("http://localhost:5000/api/departments")
      .then((r) => r.json())
      .then((data) => setDepartments(data));

    fetch("http://localhost:5000/api/positions")
      .then((r) => r.json())
      .then((data) => setPositions(data));
  };

  // Hàm gửi dữ liệu form lên backend Flask
  const handleSubmit = (e) => {
    e.preventDefault(); // Ngăn form reload trang
    fetch("http://localhost:5000/api/employees", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(form),
    })
      .then((r) => r.json())
      .then((res) => {
        alert(res.msg);
        if (res.status === "success") {
          nav("/");
        }
      });
  };

  useEffect(() => {
    loadDropdowns();
  }, []);

  return (
    <div>
      <h3>Add New Employee</h3>
      <form onSubmit={handleSubmit} className="card p-4 mt-3">
        <label>Full Name</label>
        <input
          id="FullName"
          className="form-control mb-2"
          value={form.FullName}
          onChange={handleChange}
          required
        />

        <label>Date of Birth</label>
        <input
          type="date"
          id="DateOfBirth"
          className="form-control mb-2"
          value={form.DateOfBirth}
          onChange={handleChange}
          required
        />

        <label>Gender</label>
        <select
          id="Gender"
          className="form-control mb-2"
          value={form.Gender}
          onChange={handleChange}
          required
        >
          <option value="">-- Select Gender --</option>
          <option>Nam</option>
          <option>Nữ</option>
          <option>Khác</option>
        </select>

        <label>Phone Number</label>
        <input
          id="PhoneNumber"
          className="form-control mb-2"
          value={form.PhoneNumber}
          onChange={handleChange}
          required
        />

        <label>Email</label>
        <input
          type="email"
          id="Email"
          className="form-control mb-2"
          value={form.Email}
          onChange={handleChange}
          required
        />

        <label>Hire Date</label>
        <input
          type="date"
          id="HireDate"
          className="form-control mb-2"
          value={form.HireDate}
          onChange={handleChange}
          required
        />

        <label>Department</label>
        <select
          id="DepartmentID"
          className="form-control mb-2"
          value={form.DepartmentID}
          onChange={handleChange}
        >
          <option value="">-- Select Department --</option>
          {departments.map((d) => (
            <option key={d.DepartmentID} value={d.DepartmentID}>
              {d.DepartmentName}
            </option>
          ))}
        </select>

        <label>Position</label>
        <select
          id="PositionID"
          className="form-control mb-2"
          value={form.PositionID}
          onChange={handleChange}
        >
          <option value="">-- Select Position --</option>
          {positions.map((p) => (
            <option key={p.PositionID} value={p.PositionID}>
              {p.PositionName}
            </option>
          ))}
        </select>

        <label>Status</label>
        <select
          id="Status"
          className="form-control mb-2"
          value={form.Status}
          onChange={handleChange}
        >
          <option value="Active">Active</option>
          <option value="Inactive">Inactive</option>
        </select>

        <button className="btn btn-primary mt-2">Add Employee</button>
      </form>
    </div>
  );
}
