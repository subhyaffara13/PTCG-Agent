
def float_schema(
    *,
    allow_inf_nan: bool | None = None,
    multiple_of: float | None = None,
    le: float | None = None,
    ge: float | None = None,
    lt: float | None = None,
    gt: float | None = None,
    strict: bool | None = None,
    ref: str | None = None,
    metadata: dict[str, Any] | None = None,
    serialization: SerSchema | None = None,
) -> FloatSchema:
    """
    Returns a schema that matches a float value, e.g.:

    ```py
    from pydantic_core import SchemaValidator, core_schema

    schema = core_schema.float_schema(le=0.8, ge=0.2)
    v = SchemaValidator(schema)
    assert v.validate_python('0.5') == 0.5
    ```

    Args:
        allow_inf_nan: Whether to allow inf and nan values
        multiple_of: The value must be a multiple of this number
        le: The value must be less than or equal to this number
        ge: The value must be greater than or equal to this number
        lt: The value must be strictly less than this number
        gt: The value must be strictly greater than this number
        strict: Whether the value should be a float or a value that can be converted to a float
        ref: optional unique identifier of the schema, used to reference the schema in other places
        metadata: Any other information you want to include with the schema, not used by pydantic-core
        serialization: Custom serialization schema
    """
    return _dict_not_none(
        type='float',
        allow_inf_nan=allow_inf_nan,
        multiple_of=multiple_of,
        le=le,
        ge=ge,
        lt=lt,
        gt=gt,
        strict=strict,
        ref=ref,
        metadata=metadata,
        serialization=serialization,
    )

