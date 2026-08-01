
def time_schema(
    *,
    strict: bool | None = None,
    le: time | None = None,
    ge: time | None = None,
    lt: time | None = None,
    gt: time | None = None,
    tz_constraint: Literal['aware', 'naive'] | int | None = None,
    microseconds_precision: Literal['truncate', 'error'] = 'truncate',
    ref: str | None = None,
    metadata: dict[str, Any] | None = None,
    serialization: SerSchema | None = None,
) -> TimeSchema:
    """
    Returns a schema that matches a time value, e.g.:

    ```py
    from datetime import time
    from pydantic_core import SchemaValidator, core_schema

    schema = core_schema.time_schema(le=time(12, 0, 0), ge=time(6, 0, 0))
    v = SchemaValidator(schema)
    assert v.validate_python(time(9, 0, 0)) == time(9, 0, 0)
    ```

    Args:
        strict: Whether the value should be a time or a value that can be converted to a time
        le: The value must be less than or equal to this time
        ge: The value must be greater than or equal to this time
        lt: The value must be strictly less than this time
        gt: The value must be strictly greater than this time
        tz_constraint: The value must be timezone aware or naive, or an int to indicate required tz offset
        microseconds_precision: The behavior when seconds have more than 6 digits or microseconds is too large
        ref: optional unique identifier of the schema, used to reference the schema in other places
        metadata: Any other information you want to include with the schema, not used by pydantic-core
        serialization: Custom serialization schema
    """
    return _dict_not_none(
        type='time',
        strict=strict,
        le=le,
        ge=ge,
        lt=lt,
        gt=gt,
        tz_constraint=tz_constraint,
        microseconds_precision=microseconds_precision,
        ref=ref,
        metadata=metadata,
        serialization=serialization,
    )

