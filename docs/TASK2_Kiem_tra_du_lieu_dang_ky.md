# TASK2 Kiem tra du lieu dang ky
Người thực hiện: Trần Văn Mỹ  |  Dự án: Gia sư AI  |  Công nghệ: Python, FastAPI, MySQL

## Task 2 – Kiểm tra dữ liệu đăng ký API (2 điểm)
File: `app/schemas.py` (class `RegisterRequest`)

| Trường | Quy tắc |
|---|---|
| full_name | Bắt buộc, 2–100 ký tự, tự cắt khoảng trắng thừa |
| email | Bắt buộc, đúng định dạng, tối đa 255 ký tự, tự chuyển chữ thường |
| password | Bắt buộc, theo quy tắc Task 3 |
| confirm_password | Bắt buộc, phải trùng password |

**Test case (đều PASS bằng `python -m pytest -q`)**
| # | Đầu vào | Kết quả mong đợi |
|---|---|---|
| 1 | Dữ liệu hợp lệ | 201 |
| 2 | Thiếu trường / sai kiểu dữ liệu | 422, báo lỗi từng trường |
| 3 | Email `abc@`, `abc.com`, rỗng | 422, lỗi email |
| 4 | confirm_password khác password | 422, lỗi confirm_password |
| 5 | Mật khẩu `123` | 422, lỗi password |
| 6 | Email trùng (khác hoa/thường) | 409 |
| 7 | JSON hỏng | 400 |
