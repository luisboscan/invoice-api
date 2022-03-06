from collections import namedtuple

ErrorCode = namedtuple('ErrorCode', ['code', 'message'])

invalid_request = ErrorCode(code='400', message='Invalid Request')
malformed_request = ErrorCode(code='400-001', message='Malformed request body')
missing_field = ErrorCode(code='400-002', message=None)
empty_field = ErrorCode(code='400-003', message=None)
empty_list = ErrorCode(code='400-004', message=None)
invalid_format = ErrorCode(code='400-005', message=None)
invalid_value = ErrorCode(code='400-006', message=None)
duplicate_list = ErrorCode(code='400-007', message=None)
resource_not_found = ErrorCode(code='404', message='Resource Not Found')
internal_server_error = ErrorCode(code='500', message='Internal Server Error')
