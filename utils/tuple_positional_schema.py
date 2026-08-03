from typing import Any

def tuple_positional_schema(
    items_schema: list[CoreSchema],
    *,
    extras_schema: CoreSchema | None = None,
    strict: bool | None = None,
    ref: str | None = None,
    metadata: dict[str, Any] | None = None,
    serialization: IncExSeqOrElseSerSchema | None = None,
) -> TupleSchema:
    """
    Returns a schema that matches a tuple of schemas, e.g.:

    ```py
    from pydantic_core import SchemaValidator, core_schema

    schema = core_schema.tuple_positional_schema(
        [core_schema.int_schema(), core_schema.str_schema()]
    )
    v = SchemaValidator(schema)
    assert v.validate_python((1, 'hello')) == (1, 'hello')
    ```

    Args:
        items_schema: The value must be a tuple with items that match these schemas
        extras_schema: The value must be a tuple with items that match this schema
            This was inspired by JSON schema's `prefixItems` and `items` fields.
            In python's `typing.Tuple`, you can't specify a type for "extra" items -- they must all be the same type
            if the length is variable. So this field won't be set from a `typing.Tuple` annotation on a pydantic model.
        strict: The value must be a tuple with exactly this many items
        ref: optional unique identifier of the schema, used to reference the schema in other places
        metadata: Any other information you want to include with the schema, not used by pydantic-core
        serialization: Custom serialization schema
    """
    if extras_schema is not None:
        variadic_item_index = len(items_schema)
        items_schema = items_schema + [extras_schema]
    else:
        variadic_item_index = None
    return tuple_schema(
        items_schema=items_schema,
        variadic_item_index=variadic_item_index,
        strict=strict,
        ref=ref,
        metadata=metadata,
        serialization=serialization,
    )

