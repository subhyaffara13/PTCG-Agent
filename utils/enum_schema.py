
def enum_schema(
    cls: Any,
    members: list[Any],
    *,
    sub_type: Literal['str', 'int', 'float'] | None = None,
    missing: Callable[[Any], Any] | None = None,
    strict: bool | None = None,
    ref: str | None = None,
    metadata: dict[str, Any] | None = None,
    serialization: SerSchema | None = None,
) -> EnumSchema:
    """
    Returns a schema that matches an enum value, e.g.:

    ```py
    from enum import Enum
    from pydantic_core import SchemaValidator, core_schema

    class Color(Enum):
        RED = 1
        GREEN = 2
        BLUE = 3

    schema = core_schema.enum_schema(Color, list(Color.__members__.values()))
    v = SchemaValidator(schema)
    assert v.validate_python(2) is Color.GREEN
    ```

    Args:
        cls: The enum class
        members: The members of the enum, generally `list(MyEnum.__members__.values())`
        sub_type: The type of the enum, either 'str' or 'int' or None for plain enums
        missing: A function to use when the value is not found in the enum, from `_missing_`
        strict: Whether to use strict mode, defaults to False
        ref: optional unique identifier of the schema, used to reference the schema in other places
        metadata: Any other information you want to include with the schema, not used by pydantic-core
        serialization: Custom serialization schema
    """
    return _dict_not_none(
        type='enum',
        cls=cls,
        members=members,
        sub_type=sub_type,
        missing=missing,
        strict=strict,
        ref=ref,
        metadata=metadata,
        serialization=serialization,
    )

