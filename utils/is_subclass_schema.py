
def is_subclass_schema(
    cls: type[Any],
    *,
    cls_repr: str | None = None,
    ref: str | None = None,
    metadata: dict[str, Any] | None = None,
    serialization: SerSchema | None = None,
) -> IsInstanceSchema:
    """
    Returns a schema that checks if a value is a subtype of a class, equivalent to python's `issubclass` method, e.g.:

    ```py
    from pydantic_core import SchemaValidator, core_schema

    class A:
        pass

    class B(A):
        pass

    schema = core_schema.is_subclass_schema(cls=A)
    v = SchemaValidator(schema)
    v.validate_python(B)
    ```

    Args:
        cls: The value must be a subclass of this class
        cls_repr: If provided this string is used in the validator name instead of `repr(cls)`
        ref: optional unique identifier of the schema, used to reference the schema in other places
        metadata: Any other information you want to include with the schema, not used by pydantic-core
        serialization: Custom serialization schema
    """
    return _dict_not_none(
        type='is-subclass', cls=cls, cls_repr=cls_repr, ref=ref, metadata=metadata, serialization=serialization
    )

