"""Chuyen loi thanh JSON thong nhat (Task 2 dung de tra loi kiem tra du lieu)."""
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from .errors import AppError


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(AppError)
    async def app_error_handler(request: Request, exc: AppError):
        return JSONResponse(
            status_code=exc.status,
            content={"success": False, "code": exc.code, "message": exc.message},
        )

    @app.exception_handler(RequestValidationError)
    async def validation_handler(request: Request, exc: RequestValidationError):
        """Gom loi ve dang { truong: [thong bao, ...] } bang tieng Viet."""
        errors: dict[str, list[str]] = {}
        invalid_json = False
        for err in exc.errors():
            loc, etype = err["loc"], err["type"]
            if etype == "json_invalid":
                invalid_json = True
                continue
            if loc and loc[0] == "body" and len(loc) == 1:
                errors.setdefault("body", []).append("Body phải là JSON object")
                continue
            field = str(loc[-1])
            if etype == "missing":
                msgs = [f"Thiếu trường {field}"]
            elif etype == "string_type":
                msgs = [f"{field} phải là chuỗi ký tự"]
            elif etype == "value_error":
                msgs = err["msg"].removeprefix("Value error, ").split("\n")
            else:
                msgs = [err["msg"]]
            errors.setdefault(field, []).extend(msgs)

        if invalid_json:
            return JSONResponse(
                status_code=400,
                content={"success": False, "code": "INVALID_JSON", "message": "JSON không hợp lệ"},
            )
        return JSONResponse(
            status_code=422,
            content={
                "success": False,
                "code": "VALIDATION_ERROR",
                "message": "Dữ liệu đăng ký không hợp lệ",
                "errors": errors,
            },
        )
