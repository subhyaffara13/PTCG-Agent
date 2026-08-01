
def model_parse(model: type[_ModelT], data: Any) -> _ModelT:
    if PYDANTIC_V1:
        return model.parse_obj(data)  # pyright: ignore[reportDeprecated]
    return model.model_validate(data)

