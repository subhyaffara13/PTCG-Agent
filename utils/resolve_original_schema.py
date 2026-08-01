
def resolve_original_schema(schema: CoreSchema, definitions: _Definitions) -> CoreSchema | None:
    if schema['type'] == 'definition-ref':
        return definitions.get_schema_from_ref(schema['schema_ref'])
    elif schema['type'] == 'definitions':
        return schema['schema']
    else:
        return schema

