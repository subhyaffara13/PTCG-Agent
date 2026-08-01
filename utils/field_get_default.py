
def field_get_default(field: FieldInfo) -> Any:
    value = field.get_default()
    if PYDANTIC_V1:
        return value
    from pydantic_core import PydanticUndefined

    if value == PydanticUndefined:
        return None
    return value

