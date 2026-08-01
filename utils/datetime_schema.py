
def datetime_schema(
    *,
    strict: bool | None = None,
    le: datetime | None = None,
    ge: datetime | None = None,
    lt: datetime | None = None,
    gt: datetime | None = None,
    now_op: Literal['past', 'future'] | None = None,
    tz_constraint: Literal['aware', 'naive'] | int | None = None,
    now_utc_offset: int | None = None,
    microseconds_precision: Literal['truncate', 'error'] = 'truncate',
    ref: str | None = None,
    metadata: dict[str, Any] | None = None,
    serialization: SerSchema | None = None,
) -> DatetimeSchema:
    """
    Returns a schema that matches a datetime value, e.g.:

    ```py
    from datetime import datetime
    from pydantic_core import SchemaValidator, core_schema

    schema = core_schema.datetime_schema()
    v = SchemaValidator(schema)
    now = datetime.now()
    assert v.validate_python(str(now)) == now
    ```

    Args:
        strict: Whether the value should be a datetime or a value that can be converted to a datetime
        le: The value must be less than or equal to this datetime
        ge: The value must be greater than or equal to this datetime
        lt: The value must be strictly less than this datetime
        gt: The value must be strictly greater than this datetime
        now_op: The value must be in the past or future relative to the current datetime
        tz_constraint: The value must be timezone aware or naive, or an int to indicate required tz offset
            TODO: use of a tzinfo where offset changes based on the datetime is not yet supported
        now_utc_offset: The value must be in the past or future relative to the current datetime with this utc offset
        microseconds_precision: The behavior when seconds have more than 6 digits or microseconds is too large
        ref: optional unique identifier of the schema, used to reference the schema in other places
        metadata: Any other information you want to include with the schema, not used by pydantic-core
        serialization: Custom serialization schema
    """
    return _dict_not_none(
        type='datetime',
        strict=strict,
        le=le,
        ge=ge,
        lt=lt,
        gt=gt,
        now_op=now_op,
        tz_constraint=tz_constraint,
        now_utc_offset=now_utc_offset,
        microseconds_precision=microseconds_precision,
        ref=ref,
        metadata=metadata,
        serialization=serialization,
    )

