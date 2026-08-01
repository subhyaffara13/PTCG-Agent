
def _construct_field(value: object, field: FieldInfo, key: str) -> object:
    if value is None:
        return field_get_default(field)

    if PYDANTIC_V1:
        type_ = cast(type, field.outer_type_)  # type: ignore
    else:
        type_ = field.annotation  # type: ignore

    if type_ is None:
        raise RuntimeError(f"Unexpected field type is None for {key}")

    return construct_type(value=value, type_=type_, metadata=getattr(field, "metadata", None))

