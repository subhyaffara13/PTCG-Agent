
def model_json(model: pydantic.BaseModel, *, indent: int | None = None) -> str:
    if PYDANTIC_V1:
        return model.json(indent=indent)  # type: ignore
    return model.model_dump_json(indent=indent)

