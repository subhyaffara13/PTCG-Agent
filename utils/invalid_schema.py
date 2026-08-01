
def invalid_schema(ref: str | None = None, metadata: dict[str, Any] | None = None) -> InvalidSchema:
    """
    Returns an invalid schema, used to indicate that a schema is invalid.

    Args:
        ref: optional unique identifier of the schema, used to reference the schema in other places
        metadata: Any other information you want to include with the schema, not used by pydantic-core
    """

    return _dict_not_none(type='invalid', ref=ref, metadata=metadata)

