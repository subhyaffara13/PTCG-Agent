
def model_fields_schema(
    fields: dict[str, ModelField],
    *,
    model_name: str | None = None,
    computed_fields: list[ComputedField] | None = None,
    strict: bool | None = None,
    extras_schema: CoreSchema | None = None,
    extras_keys_schema: CoreSchema | None = None,
    extra_behavior: ExtraBehavior | None = None,
    from_attributes: bool | None = None,
    ref: str | None = None,
    metadata: dict[str, Any] | None = None,
    serialization: SerSchema | None = None,
) -> ModelFieldsSchema:
    """
    Returns a schema that matches the fields of a Pydantic model, e.g.:

    ```py
    from pydantic_core import SchemaValidator, core_schema

    wrapper_schema = core_schema.model_fields_schema(
        {'a': core_schema.model_field(core_schema.str_schema())}
    )
    v = SchemaValidator(wrapper_schema)
    print(v.validate_python({'a': 'hello'}))
    #> ({'a': 'hello'}, None, {'a'})
    ```

    Args:
        fields: The fields of the model
        model_name: The name of the model, used for error messages, defaults to "Model"
        computed_fields: Computed fields to use when serializing the model, only applies when directly inside a model
        strict: Whether the model is strict
        extras_schema: The schema to use when validating extra input data
        extras_keys_schema: The schema to use when validating the keys of extra input data
        ref: optional unique identifier of the schema, used to reference the schema in other places
        metadata: Any other information you want to include with the schema, not used by pydantic-core
        extra_behavior: The extra behavior to use for the model fields
        from_attributes: Whether the model fields should be populated from attributes
        serialization: Custom serialization schema
    """
    return _dict_not_none(
        type='model-fields',
        fields=fields,
        model_name=model_name,
        computed_fields=computed_fields,
        strict=strict,
        extras_schema=extras_schema,
        extras_keys_schema=extras_keys_schema,
        extra_behavior=extra_behavior,
        from_attributes=from_attributes,
        ref=ref,
        metadata=metadata,
        serialization=serialization,
    )

