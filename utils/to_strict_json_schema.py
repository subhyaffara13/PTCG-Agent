from typing import Any

def to_strict_json_schema(model: type[pydantic.BaseModel] | pydantic.TypeAdapter[Any]) -> dict[str, Any]:
    if inspect.isclass(model) and is_basemodel_type(model):
        schema = model_json_schema(model)
    elif (not PYDANTIC_V1) and isinstance(model, pydantic.TypeAdapter):
        schema = model.json_schema()
    else:
        raise TypeError(f"Non BaseModel types are only supported with Pydantic v2 - {model}")

    return _ensure_strict_json_schema(schema, path=(), root=schema)

