
def model_field(
    schema: CoreSchema,
    *,
    validation_alias: str | list[str | int] | list[list[str | int]] | None = None,
    serialization_alias: str | None = None,
    serialization_exclude: bool | None = None,
    serialization_exclude_if: Callable[[Any], bool] | None = None,
    frozen: bool | None = None,
    metadata: dict[str, Any] | None = None,
) -> ModelField:
    """
    Returns a schema for a model field, e.g.:

    ```py
    from pydantic_core import core_schema

    field = core_schema.model_field(schema=core_schema.int_schema())
    ```

    Args:
        schema: The schema to use for the field
        validation_alias: The alias(es) to use to find the field in the validation data
        serialization_alias: The alias to use as a key when serializing
        serialization_exclude: Whether to exclude the field when serializing
        serialization_exclude_if: A Callable that determines whether to exclude a field during serialization based on its value.
        frozen: Whether the field is frozen
        metadata: Any other information you want to include with the schema, not used by pydantic-core
    """
    return _dict_not_none(
        type='model-field',
        schema=schema,
        validation_alias=validation_alias,
        serialization_alias=serialization_alias,
        serialization_exclude=serialization_exclude,
        serialization_exclude_if=serialization_exclude_if,
        frozen=frozen,
        metadata=metadata,
    )

