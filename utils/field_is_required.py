
def field_is_required(field: FieldInfo) -> bool:
    if PYDANTIC_V1:
        return field.required  # type: ignore
    return field.is_required()

