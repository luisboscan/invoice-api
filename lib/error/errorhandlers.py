import logging

from flask import jsonify, Blueprint
from werkzeug.exceptions import HTTPException

from lib.error.apierrors import RootApiError
from lib.error.errorcodes import resource_not_found, internal_server_error
from lib.error.errors import NotFoundError

error_handlers = Blueprint('error_handlers', __name__)


@error_handlers.app_errorhandler(NotFoundError)
def handle_not_found_error(e):
    return jsonify({
        'error': {
            "code": resource_not_found.code,
            "message": resource_not_found.message,
        }
    }), int(resource_not_found.code)


@error_handlers.app_errorhandler(RootApiError)
def handle_root_api_error(e: RootApiError):
    return jsonify({
        'error': e.to_dict()
    }), e.http_status_code


@error_handlers.app_errorhandler(Exception)
def handle_exception(e):
    logging.error(e, exc_info=e)
    if isinstance(e, HTTPException):
        return e

    return jsonify({
        'error': {
            "code": internal_server_error.code,
            "message": internal_server_error.message,
        }
    }), int(internal_server_error.code)
