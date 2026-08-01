
def definitions_schema(schema: CoreSchema, definitions: list[CoreSchema]) -> DefinitionsSchema:
    """
    Build a schema that contains both an inner schema and a list of definitions which can be used
    within the inner schema.

    ```py
    from pydantic_core import SchemaValidator, core_schema

    schema = core_schema.definitions_schema(
        core_schema.list_schema(core_schema.definition_reference_schema('foobar')),
        [core_schema.int_schema(ref='foobar')],
    )
    v = SchemaValidator(schema)
    assert v.validate_python([1, 2, '3']) == [1, 2, 3]
    ```

    Args:
        schema: The inner schema
        definitions: List of definitions which can be referenced within inner schema
    """
    return DefinitionsSchema(type='definitions', schema=schema, definitions=definitions)

