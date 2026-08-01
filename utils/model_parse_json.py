
def model_parse_json(model: type[_ModelT], data: str | bytes) -> _ModelT:
    if PYDANTIC_V1:
        return model.parse_raw(data)  # pyright: ignore[reportDeprecated]
    return model.model_validate_json(data)

