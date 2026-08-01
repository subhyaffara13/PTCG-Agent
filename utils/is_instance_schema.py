
def is_instance_schema(
    cls: Any,
    *,
    cls_repr: str | None = None,
    ref: str | None = None,
    metadata: dict[str, Any] | None = None,
    serialization: SerSchema | None = None,
) -> IsInstanceSchema:
    """
    Returns a schema that checks if a value is an instance of a class, equivalent to python's `isinstance` method, e.g.:

    ```py
    from pydantic_core import SchemaValidator, core_schema

    class A:
        pass

    schema = core_schema.is_instance_schema(cls=A)
    v = SchemaValidator(schema)
    v.validate_python(A())
    ```

    Args:
        cls: The value must be an instance of this class
        cls_repr: If provided this string is used in the validator name instead of `repr(cls)`
        ref: optional unique identifier of the schema, used to reference the schema in other places
        metadata: Any other information you want to include with the schema, not used by pydantic-core
        serialization: Custom serialization schema
    """
    return _dict_not_none(
        type='is-instance', cls=cls, cls_repr=cls_repr, ref=ref, metadata=metadata, serialization=serialization
    )

