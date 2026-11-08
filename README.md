# Task 2 – Kiểm tra dữ liệu đăng ký API (2 điểm)
Chạy được riêng, không cần MySQL.

```bash
pip install -r requirements.txt
python -m pytest -q
```
**File của task này:** `app/schemas.py` (quy tắc từng trường), `app/error_handlers.py` + `app/errors.py` (trả lỗi JSON tiếng Việt theo từng trường).

**File phụ thuộc (của Task 3):** `app/security.py` – hàm kiểm tra độ mạnh mật khẩu mà `schemas.py` gọi.

Gắn vào app FastAPI: `register_exception_handlers(app)`, rồi dùng `RegisterRequest` làm kiểu body của endpoint.
