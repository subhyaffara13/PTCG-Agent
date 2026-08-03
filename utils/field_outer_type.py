from typing import Any

def field_outer_type(field: FieldInfo) -> Any:
    if PYDANTIC_V1:
        return field.outer_type_  # type: ignore
    return field.annotation

