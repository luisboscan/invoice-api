from typing import Any, Dict, List

from lib.error import errorcodes


class ApiError(Exception):

    def __init__(self,
                 code: str,
                 message: str,
                 path: List[str] = None,
                 reasons: List['ApiError'] = None,
                 params: Dict[str, Any] = None):
        self.code = code
        self.message = message
        self.path = path
        self.reasons = reasons
        self.params = params

    def to_dict(self) -> dict:
        json_value = {
            'code': self.code,
            'message': self.message,
        }
        if self.path:
            json_value['path'] = self.path
        if self.reasons:
            json_value['reasons'] = [reason.to_dict() for reason in self.reasons]
        if self.params:
            json_value['params'] = self.params
        return json_value


class RootApiError(ApiError):

    def __init__(self,
                 http_status_code: int,
                 code: str,
                 message: str,
                 reasons: List[ApiError] = None):
        super().__init__(code=code, message=message, reasons=reasons)
        self.http_status_code = http_status_code


class InvalidRequestApiError(RootApiError):

    def __init__(self, reasons: List[ApiError]):
        super().__init__(http_status_code=int(errorcodes.invalid_request.code),
                         code=errorcodes.invalid_request.code,
                         message=errorcodes.invalid_request.message,
                         reasons=reasons)
