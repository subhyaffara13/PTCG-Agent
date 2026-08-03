from typing import Any

def json_schema(
    schema: CoreSchema | None = None,
    *,
    ref: str | None = None,
    metadata: dict[str, Any] | None = None,
    serialization: SerSchema | None = None,
) -> JsonSchema:
    """
    Returns a schema that matches a JSON value, e.g.:

    ```py
    from pydantic_core import SchemaValidator, core_schema

    dict_schema = core_schema.model_fields_schema(
        {
            'field_a': core_schema.model_field(core_schema.str_schema()),
            'field_b': core_schema.model_field(core_schema.bool_schema()),
        },
    )

    class MyModel:
        __slots__ = (
            '__dict__',
            '__pydantic_fields_set__',
            '__pydantic_extra__',
            '__pydantic_private__',
        )
        field_a: str
        field_b: bool

    json_schema = core_schema.json_schema(schema=dict_schema)
    schema = core_schema.model_schema(cls=MyModel, schema=json_schema)
    v = SchemaValidator(schema)
    m = v.validate_python('{"field_a": "hello", "field_b": true}')
    assert isinstance(m, MyModel)
    ```

    Args:
        schema: The schema to use for the JSON schema
        ref: optional unique identifier of the schema, used to reference the schema in other places
        metadata: Any other information you want to include with the schema, not used by pydantic-core
        serialization: Custom serialization schema
    """
    return _dict_not_none(type='json', schema=schema, ref=ref, metadata=metadata, serialization=serialization)

