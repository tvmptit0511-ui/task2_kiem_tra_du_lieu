"""Kiem tra dinh dang JSON loi cua Task 2 bang 1 app nho (khong can DB)."""
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.error_handlers import register_exception_handlers
from app.schemas import RegisterRequest

mini = FastAPI()
register_exception_handlers(mini)


@mini.post("/check")
def check(payload: RegisterRequest):
    return payload


c = TestClient(mini)
OK = {"full_name": "Trần Văn Mỹ", "email": "my@example.com",
      "password": "Abcdef1@", "confirm_password": "Abcdef1@"}


def test_hop_le():
    assert c.post("/check", json=OK).status_code == 200


def test_loi_theo_tung_truong():
    r = c.post("/check", json={**OK, "email": "x", "password": "123"})
    assert r.status_code == 422
    assert r.json()["errors"]["email"] == ["Email không hợp lệ"]
    assert len(r.json()["errors"]["password"]) >= 3


def test_thieu_truong_va_sai_kieu():
    r = c.post("/check", json={"full_name": 123})
    assert r.status_code == 422
    assert {"full_name", "email", "password", "confirm_password"} <= set(r.json()["errors"])


def test_confirm_khong_khop():
    r = c.post("/check", json={**OK, "confirm_password": "Khac1@abc"})
    assert r.json()["errors"]["confirm_password"] == ["Mật khẩu xác nhận không khớp"]


def test_json_hong():
    r = c.post("/check", content="{bad", headers={"Content-Type": "application/json"})
    assert r.status_code == 400 and r.json()["code"] == "INVALID_JSON"
