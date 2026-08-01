
def _parse_content(response_format: type[ResponseFormatT], content: str) -> ResponseFormatT:
    if is_basemodel_type(response_format):
        return cast(ResponseFormatT, model_parse_json(response_format, content))

    if is_dataclass_like_type(response_format):
        if PYDANTIC_V1:
            raise TypeError(f"Non BaseModel types are only supported with Pydantic v2 - {response_format}")

        return pydantic.TypeAdapter(response_format).validate_json(content)

    raise TypeError(f"Unable to automatically parse response format type {response_format}")

