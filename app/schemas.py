"""Task 2 - Kiem tra du lieu dang ky (Pydantic)."""
import re
from datetime import datetime

from pydantic import BaseModel, ConfigDict, ValidationInfo, field_validator

from .security import validate_password_strength

EMAIL_RE = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]{2,}$")


class RegisterRequest(BaseModel):
    full_name: str
    email: str
    password: str
    confirm_password: str

    @field_validator("full_name")
    @classmethod
    def check_full_name(cls, v: str) -> str:
        v = re.sub(r"\s+", " ", v.strip())
        if not v:
            raise ValueError("Họ tên không được để trống")
        if not 2 <= len(v) <= 100:
            raise ValueError("Họ tên từ 2 đến 100 ký tự")
        return v

    @field_validator("email")
    @classmethod
    def check_email(cls, v: str) -> str:
        v = v.strip().lower()
        if not v:
            raise ValueError("Email không được để trống")
        if len(v) > 255 or not EMAIL_RE.match(v):
            raise ValueError("Email không hợp lệ")
        return v

    @field_validator("password")
    @classmethod
    def check_password(cls, v: str) -> str:
        if v == "":
            raise ValueError("Mật khẩu không được để trống")
        errors = validate_password_strength(v)
        if errors:
            raise ValueError("\n".join(errors))  # nhieu loi -> tach bang \n
        return v

    @field_validator("confirm_password")
    @classmethod
    def check_confirm(cls, v: str, info: ValidationInfo) -> str:
        if v == "":
            raise ValueError("Vui lòng nhập lại mật khẩu")
        password = info.data.get("password")
        if password is not None and v != password:
            raise ValueError("Mật khẩu xác nhận không khớp")
        return v


class UserOut(BaseModel):
    """Du lieu tra ve - KHONG co password / password_hash."""
    model_config = ConfigDict(from_attributes=True)

    id: int
    full_name: str
    email: str
    role: str
    status: str
    created_at: datetime
