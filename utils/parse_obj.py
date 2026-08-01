
def parse_obj(model: type[_ModelT], value: object) -> _ModelT:
    if PYDANTIC_V1:
        return cast(_ModelT, model.parse_obj(value))  # pyright: ignore[reportDeprecated, reportUnnecessaryCast]
    else:
        return model.model_validate(value)

