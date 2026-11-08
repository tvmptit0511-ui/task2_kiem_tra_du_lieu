class AppError(Exception):
    """Loi nghiep vu co ma HTTP + ma loi rieng."""

    def __init__(self, status: int, code: str, message: str):
        self.status, self.code, self.message = status, code, message
