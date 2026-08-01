
def get_model_config(model: type[pydantic.BaseModel]) -> Any:
    if PYDANTIC_V1:
        return model.__config__  # type: ignore
    return model.model_config

