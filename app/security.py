"""Task 3 - Bam va kiem tra mat khau (bcrypt)."""
import os
import re

import bcrypt


def _cost() -> int:
    return int(os.getenv("BCRYPT_COST", "12"))


def validate_password_strength(password: str) -> list[str]:
    """Tra ve danh sach loi (rong = hop le).

    Quy tac: 8-64 ky tu, co chu hoa, chu thuong, so, ky tu dac biet,
    khong co khoang trang, toi da 72 byte (gioi han cua bcrypt).
    """
    errors: list[str] = []
    if not isinstance(password, str):
        return ["Mật khẩu phải là chuỗi ký tự"]
    if len(password) < 8:
        errors.append("Mật khẩu tối thiểu 8 ký tự")
    if len(password) > 64:
        errors.append("Mật khẩu tối đa 64 ký tự")
    if re.search(r"\s", password):
        errors.append("Mật khẩu không được chứa khoảng trắng")
    if not re.search(r"[a-z]", password):
        errors.append("Mật khẩu cần có chữ thường")
    if not re.search(r"[A-Z]", password):
        errors.append("Mật khẩu cần có chữ hoa")
    if not re.search(r"[0-9]", password):
        errors.append("Mật khẩu cần có chữ số")
    if not re.search(r"[^A-Za-z0-9\s]", password):
        errors.append("Mật khẩu cần có ký tự đặc biệt")
    if len(password.encode("utf-8")) > 72:
        errors.append("Mật khẩu quá dài (tối đa 72 byte)")
    return errors


def hash_password(plain: str) -> str:
    """Bam mat khau bang bcrypt (tu sinh salt moi lan)."""
    return bcrypt.hashpw(plain.encode("utf-8"), bcrypt.gensalt(rounds=_cost())).decode("utf-8")


def verify_password(plain: str, hashed: str) -> bool:
    """So khop mat khau nhap vao voi hash da luu. Khong bao gio nem loi."""
    if not isinstance(plain, str) or not isinstance(hashed, str):
        return False
    try:
        return bcrypt.checkpw(plain.encode("utf-8"), hashed.encode("utf-8"))
    except ValueError:
        return False
