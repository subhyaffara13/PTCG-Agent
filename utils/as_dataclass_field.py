import sys
from typing import Any

def as_dataclass_field(pydantic_field: FieldInfo) -> dataclasses.Field[Any]:
    field_args: dict[str, Any] = {'default': pydantic_field}

    # Needed because if `doc` is set, the dataclass slots will be a dict (field name -> doc) instead of a tuple:
    if sys.version_info >= (3, 14) and pydantic_field.description is not None:
        field_args['doc'] = pydantic_field.description

    # Needed as the stdlib dataclass module processes kw_only in a specific way during class construction:
    if sys.version_info >= (3, 10) and pydantic_field.kw_only is not None:
        field_args['kw_only'] = pydantic_field.kw_only

    # Needed as the stdlib dataclass modules generates `__repr__()` during class construction:
    if pydantic_field.repr is not True:
        field_args['repr'] = pydantic_field.repr

    return dataclasses.field(**field_args)

