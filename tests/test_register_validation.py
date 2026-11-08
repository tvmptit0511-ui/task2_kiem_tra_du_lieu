import pytest
from pydantic import ValidationError

from app.schemas import RegisterRequest

OK = {"full_name": "  Trần   Văn Mỹ ", "email": " Van.My@Example.COM ",
      "password": "Abcdef1@", "confirm_password": "Abcdef1@"}


def test_hop_le_va_chuan_hoa():
    r = RegisterRequest(**OK)
    assert r.full_name == "Trần Văn Mỹ"
    assert r.email == "van.my@example.com"


@pytest.mark.parametrize("email", ["abc@", "abc.com", "a b@c.com", ""])
def test_email_sai(email):
    with pytest.raises(ValidationError):
        RegisterRequest(**{**OK, "email": email})


def test_confirm_khong_khop():
    with pytest.raises(ValidationError):
        RegisterRequest(**{**OK, "confirm_password": "Khac1@abc"})


def test_thieu_truong():
    with pytest.raises(ValidationError) as e:
        RegisterRequest()
    assert len(e.value.errors()) == 4
