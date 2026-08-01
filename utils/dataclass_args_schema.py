
def dataclass_args_schema(
    dataclass_name: str,
    fields: list[DataclassField],
    *,
    computed_fields: list[ComputedField] | None = None,
    collect_init_only: bool | None = None,
    ref: str | None = None,
    metadata: dict[str, Any] | None = None,
    serialization: SerSchema | None = None,
    extra_behavior: ExtraBehavior | None = None,
) -> DataclassArgsSchema:
    """
    Returns a schema for validating dataclass arguments, e.g.:

    ```py
    from pydantic_core import SchemaValidator, core_schema

    field_a = core_schema.dataclass_field(
        name='a', schema=core_schema.str_schema(), kw_only=False
    )
    field_b = core_schema.dataclass_field(
        name='b', schema=core_schema.bool_schema(), kw_only=False
    )
    schema = core_schema.dataclass_args_schema('Foobar', [field_a, field_b])
    v = SchemaValidator(schema)
    assert v.validate_python({'a': 'hello', 'b': True}) == ({'a': 'hello', 'b': True}, None)
    ```

    Args:
        dataclass_name: The name of the dataclass being validated
        fields: The fields to use for the dataclass
        computed_fields: Computed fields to use when serializing the dataclass
        collect_init_only: Whether to collect init only fields into a dict to pass to `__post_init__`
        ref: optional unique identifier of the schema, used to reference the schema in other places
        metadata: Any other information you want to include with the schema, not used by pydantic-core
        serialization: Custom serialization schema
        extra_behavior: How to handle extra fields
    """
    return _dict_not_none(
        type='dataclass-args',
        dataclass_name=dataclass_name,
        fields=fields,
        computed_fields=computed_fields,
        collect_init_only=collect_init_only,
        ref=ref,
        metadata=metadata,
        serialization=serialization,
        extra_behavior=extra_behavior,
    )

