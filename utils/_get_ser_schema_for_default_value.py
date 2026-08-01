
def _get_ser_schema_for_default_value(schema: CoreSchema) -> core_schema.PlainSerializerFunctionSerSchema | None:
    """Get a `'function-plain'` serialization schema that can be used to serialize a default value.

    This takes into account having the serialization schema nested under validation schema(s).
    """
    if (
        (ser_schema := schema.get('serialization'))
        and ser_schema['type'] == 'function-plain'
        and not ser_schema.get('info_arg')
    ):
        return ser_schema
    if _core_utils.is_function_with_inner_schema(schema):
        return _get_ser_schema_for_default_value(schema['schema'])

