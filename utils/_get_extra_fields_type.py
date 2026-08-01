
def _get_extra_fields_type(cls: type[pydantic.BaseModel]) -> type | None:
    if PYDANTIC_V1:
        # TODO
        return None

    schema = cls.__pydantic_core_schema__
    if schema["type"] == "model":
        fields = schema["schema"]
        if fields["type"] == "model-fields":
            extras = fields.get("extras_schema")
            if extras and "cls" in extras:
                # mypy can't narrow the type
                return extras["cls"]  # type: ignore[no-any-return]

    return None

