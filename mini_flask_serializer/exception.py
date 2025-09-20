class BaseException(Exception):
    pass
    
class ValidationError(BaseException):
    pass


class AttributeError(ValidationError):
    pass

