class BaseException(Exception):
    pass
    
class ValidationError(BaseException):
    def __init__(self, message: str) -> None:
        super().__init__(message)


class AttributeError(BaseException):
    def __init__(self, message: str) -> None:
        super().__init__(message)