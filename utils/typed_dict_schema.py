
def typed_dict_schema(
    fields: dict[str, TypedDictField],
    *,
    cls: type[Any] | None = None,
    cls_name: str | None = None,
    computed_fields: list[ComputedField] | None = None,
    strict: bool | None = None,
    extras_schema: CoreSchema | None = None,
    extra_behavior: ExtraBehavior | None = None,
    total: bool | None = None,
    ref: str | None = None,
    metadata: dict[str, Any] | None = None,
    serialization: SerSchema | None = None,
    config: CoreConfig | None = None,
) -> TypedDictSchema:
    """
    Returns a schema that matches a typed dict, e.g.:

    ```py
    from typing_extensions import TypedDict

    from pydantic_core import SchemaValidator, core_schema

    class MyTypedDict(TypedDict):
        a: str

    wrapper_schema = core_schema.typed_dict_schema(
        {'a': core_schema.typed_dict_field(core_schema.str_schema())}, cls=MyTypedDict
    )
    v = SchemaValidator(wrapper_schema)
    assert v.validate_python({'a': 'hello'}) == {'a': 'hello'}
    ```

    Args:
        fields: The fields to use for the typed dict
        cls: The class to use for the typed dict
        cls_name: The name to use in error locations. Falls back to `cls.__name__`, or the validator name if no class
            is provided.
        computed_fields: Computed fields to use when serializing the model, only applies when directly inside a model
        strict: Whether the typed dict is strict
        extras_schema: The extra validator to use for the typed dict
        ref: optional unique identifier of the schema, used to reference the schema in other places
        metadata: Any other information you want to include with the schema, not used by pydantic-core
        extra_behavior: The extra behavior to use for the typed dict
        total: Whether the typed dict is total, otherwise uses `typed_dict_total` from config
        serialization: Custom serialization schema
    """
    return _dict_not_none(
        type='typed-dict',
        fields=fields,
        cls=cls,
        cls_name=cls_name,
        computed_fields=computed_fields,
        strict=strict,
        extras_schema=extras_schema,
        extra_behavior=extra_behavior,
        total=total,
        ref=ref,
        metadata=metadata,
        serialization=serialization,
        config=config,
    )

