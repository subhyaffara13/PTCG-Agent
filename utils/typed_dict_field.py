
def typed_dict_field(
    schema: CoreSchema,
    *,
    required: bool | None = None,
    validation_alias: str | list[str | int] | list[list[str | int]] | None = None,
    serialization_alias: str | None = None,
    serialization_exclude: bool | None = None,
    metadata: dict[str, Any] | None = None,
    serialization_exclude_if: Callable[[Any], bool] | None = None,
) -> TypedDictField:
    """
    Returns a schema that matches a typed dict field, e.g.:

    ```py
    from pydantic_core import core_schema

    field = core_schema.typed_dict_field(schema=core_schema.int_schema(), required=True)
    ```

    Args:
        schema: The schema to use for the field
        required: Whether the field is required, otherwise uses the value from `total` on the typed dict
        validation_alias: The alias(es) to use to find the field in the validation data
        serialization_alias: The alias to use as a key when serializing
        serialization_exclude: Whether to exclude the field when serializing
        serialization_exclude_if: A callable that determines whether to exclude the field when serializing based on its value.
        metadata: Any other information you want to include with the schema, not used by pydantic-core
    """
    return _dict_not_none(
        type='typed-dict-field',
        schema=schema,
        required=required,
        validation_alias=validation_alias,
        serialization_alias=serialization_alias,
        serialization_exclude=serialization_exclude,
        serialization_exclude_if=serialization_exclude_if,
        metadata=metadata,
    )

