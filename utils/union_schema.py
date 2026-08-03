from typing import Any

def union_schema(
    choices: list[CoreSchema | tuple[CoreSchema, str]],
    *,
    auto_collapse: bool | None = None,
    custom_error_type: str | None = None,
    custom_error_message: str | None = None,
    custom_error_context: dict[str, str | int] | None = None,
    mode: Literal['smart', 'left_to_right'] | None = None,
    ref: str | None = None,
    metadata: dict[str, Any] | None = None,
    serialization: SerSchema | None = None,
) -> UnionSchema:
    """
    Returns a schema that matches a union value, e.g.:

    ```py
    from pydantic_core import SchemaValidator, core_schema

    schema = core_schema.union_schema([core_schema.str_schema(), core_schema.int_schema()])
    v = SchemaValidator(schema)
    assert v.validate_python('hello') == 'hello'
    assert v.validate_python(1) == 1
    ```

    Args:
        choices: The schemas to match. If a tuple, the second item is used as the label for the case.
        auto_collapse: whether to automatically collapse unions with one element to the inner validator, default true
        custom_error_type: The custom error type to use if the validation fails
        custom_error_message: The custom error message to use if the validation fails
        custom_error_context: The custom error context to use if the validation fails
        mode: How to select which choice to return
            * `smart` (default) will try to return the choice which is the closest match to the input value
            * `left_to_right` will return the first choice in `choices` which succeeds validation
        ref: optional unique identifier of the schema, used to reference the schema in other places
        metadata: Any other information you want to include with the schema, not used by pydantic-core
        serialization: Custom serialization schema
    """
    return _dict_not_none(
        type='union',
        choices=choices,
        auto_collapse=auto_collapse,
        custom_error_type=custom_error_type,
        custom_error_message=custom_error_message,
        custom_error_context=custom_error_context,
        mode=mode,
        ref=ref,
        metadata=metadata,
        serialization=serialization,
    )

