
def get_model_fields(model: type[pydantic.BaseModel]) -> dict[str, FieldInfo]:
    if PYDANTIC_V1:
        return model.__fields__  # type: ignore
    return model.model_fields

