import json
import re
from typing import List, Union

from importlib_resources import files
import jsonschema
from jsonschema.exceptions import _Error

from lib.error import errorcodes
from lib.error.apierrors import ApiError, InvalidRequestApiError


def validate_schema(data_to_validate: dict, schema_package, schema_name: str) -> None:
    """REF: https://json-schema.org """
    schema_text = files(schema_package).joinpath(f'{schema_name}.json').read_text()
    schema = json.loads(schema_text)
    validator = jsonschema.Draft7Validator(schema)

    if not validator.is_valid(data_to_validate, schema):
        json_schema_errors = list(validator.iter_errors(data_to_validate))
        invalid_request_api_error = __map_to_api_errors(json_schema_errors)
        raise invalid_request_api_error


def __map_to_api_errors(json_schema_errors: List[_Error]) -> InvalidRequestApiError:
    reasons = list(map(__map_to_api_error, json_schema_errors))
    return InvalidRequestApiError(reasons)


def __map_to_api_error(json_schema_error: _Error) -> ApiError:
    reason = None

    if json_schema_error.validator == 'required':
        field_name = re.findall(r"'(.*?)'", json_schema_error.message)[0]
        path = list(json_schema_error.relative_path) + [field_name]
        absolute_field_name = __get_absolute_field_name_from(path)
        reason = ApiError(
            code=errorcodes.missing_field.code,
            message=f"Missing field '{absolute_field_name}'",
            path=path
        )

    elif json_schema_error.validator == 'type':
        path = list(json_schema_error.relative_path)
        absolute_field_name = __get_absolute_field_name_from(path)
        reason = ApiError(
            code=errorcodes.invalid_value.code,
            message=f"Invalid value for field '{absolute_field_name}', "
                    f"supported types: {json_schema_error.validator_value}",
            path=path
        )

    elif json_schema_error.validator == 'pattern':
        path = list(json_schema_error.relative_path)
        absolute_field_name = __get_absolute_field_name_from(path)
        if json_schema_error.validator_value == "^(?!\s*$).+":
            reason = ApiError(
                code=errorcodes.empty_field.code,
                message=f"Empty field '{absolute_field_name}'",
                path=path
            )
        else:
            reason = ApiError(
                code=errorcodes.invalid_format.code,
                message=f"Invalid format for field '{absolute_field_name}'",
                path=path,
                params={
                    'pattern': json_schema_error.validator_value
                }
            )

    elif json_schema_error.validator == 'minItems':
        path = list(json_schema_error.relative_path)
        absolute_field_name = __get_absolute_field_name_from(path)
        if json_schema_error.validator_value == 1:
            reason = ApiError(
                code=errorcodes.empty_list.code,
                message=f"There must be at least one entry for field '{absolute_field_name}'",
                path=path
            )

    elif json_schema_error.validator == 'uniqueItems':
        path = list(json_schema_error.relative_path)
        absolute_field_name = __get_absolute_field_name_from(path)
        reason = ApiError(
            code=errorcodes.duplicate_list.code,
            message=f"Field '{absolute_field_name}' cannot contain duplicate values",
            path=path
        )

    elif json_schema_error.validator == 'minimum':
        path = list(json_schema_error.relative_path)
        absolute_field_name = __get_absolute_field_name_from(path)
        reason = ApiError(
            code=errorcodes.invalid_value.code,
            message=f"Invalid value for field '{absolute_field_name}', "
                    f"value cannot be lower than: {json_schema_error.validator_value}",
            path=path
        )

    elif json_schema_error.validator == 'maximum':
        path = list(json_schema_error.relative_path)
        absolute_field_name = __get_absolute_field_name_from(path)
        reason = ApiError(
            code=errorcodes.invalid_value.code,
            message=f"Invalid value for field '{absolute_field_name}', "
                    f"value cannot be higher than: {json_schema_error.validator_value}",
            path=path
        )

    elif json_schema_error.validator == 'enum':
        path = list(json_schema_error.relative_path)
        absolute_field_name = __get_absolute_field_name_from(path)
        reason = ApiError(
            code=errorcodes.invalid_value.code,
            message=f"Invalid value for field '{absolute_field_name}', "
                    f"supported values: {json_schema_error.validator_value}",
            path=path
        )

    if reason:
        return reason
    else:
        raise Exception(f"Unsupported validator '{json_schema_error.validator}' "
                        f"w/ value '{json_schema_error.validator_value}'")


def __get_absolute_field_name_from(path: List[Union[str, int]]) -> str:
    absolute_field_name = ''
    for index, element in enumerate(path):
        if isinstance(element, int):
            absolute_field_name += f'[{element}]'
        elif index == 0:
            absolute_field_name = element
        else:
            absolute_field_name += f'.{element}'
    return absolute_field_name
