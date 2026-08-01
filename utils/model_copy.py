
def model_copy(model: _ModelT, *, deep: bool = False) -> _ModelT:
    if PYDANTIC_V1:
        return model.copy(deep=deep)  # type: ignore
    return model.model_copy(deep=deep)

