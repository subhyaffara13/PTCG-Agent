
def traverse_schema(schema: AllSchemas, context: GatherContext) -> None:
    # TODO When we drop 3.9, use a match statement to get better type checking and remove
    # file-level type ignore.
    # (the `'type'` could also be fetched in every `if/elif` statement, but this alters performance).
    schema_type = schema['type']

    if schema_type == 'definition-ref':
        traverse_definition_ref(schema, context)
        # `traverse_definition_ref` handles the possible serialization and metadata schemas:
        return
    elif schema_type == 'definitions':
        traverse_schema(schema['schema'], context)
        for definition in schema['definitions']:
            traverse_schema(definition, context)
    elif schema_type in {'list', 'set', 'frozenset', 'generator'}:
        if 'items_schema' in schema:
            traverse_schema(schema['items_schema'], context)
    elif schema_type == 'tuple':
        if 'items_schema' in schema:
            for s in schema['items_schema']:
                traverse_schema(s, context)
    elif schema_type == 'dict':
        if 'keys_schema' in schema:
            traverse_schema(schema['keys_schema'], context)
        if 'values_schema' in schema:
            traverse_schema(schema['values_schema'], context)
    elif schema_type == 'union':
        for choice in iter_union_choices(schema):
            traverse_schema(choice, context)
    elif schema_type == 'tagged-union':
        for v in schema['choices'].values():
            traverse_schema(v, context)
    elif schema_type == 'chain':
        for step in schema['steps']:
            traverse_schema(step, context)
    elif schema_type == 'lax-or-strict':
        traverse_schema(schema['lax_schema'], context)
        traverse_schema(schema['strict_schema'], context)
    elif schema_type == 'json-or-python':
        traverse_schema(schema['json_schema'], context)
        traverse_schema(schema['python_schema'], context)
    elif schema_type in {'model-fields', 'typed-dict'}:
        if 'extras_schema' in schema:
            traverse_schema(schema['extras_schema'], context)
        if 'computed_fields' in schema:
            for s in schema['computed_fields']:
                traverse_schema(s, context)
        for s in schema['fields'].values():
            traverse_schema(s, context)
    elif schema_type == 'dataclass-args':
        if 'computed_fields' in schema:
            for s in schema['computed_fields']:
                traverse_schema(s, context)
        for s in schema['fields']:
            traverse_schema(s, context)
    elif schema_type == 'arguments':
        for s in schema['arguments_schema']:
            traverse_schema(s['schema'], context)
        if 'var_args_schema' in schema:
            traverse_schema(schema['var_args_schema'], context)
        if 'var_kwargs_schema' in schema:
            traverse_schema(schema['var_kwargs_schema'], context)
    elif schema_type == 'arguments-v3':
        for s in schema['arguments_schema']:
            traverse_schema(s['schema'], context)
    elif schema_type == 'call':
        traverse_schema(schema['arguments_schema'], context)
        if 'return_schema' in schema:
            traverse_schema(schema['return_schema'], context)
    elif schema_type == 'computed-field':
        traverse_schema(schema['return_schema'], context)
    elif schema_type == 'function-before':
        if 'schema' in schema:
            traverse_schema(schema['schema'], context)
        if 'json_schema_input_schema' in schema:
            traverse_schema(schema['json_schema_input_schema'], context)
    elif schema_type == 'function-plain':
        # TODO duplicate schema types for serializers and validators, needs to be deduplicated.
        if 'return_schema' in schema:
            traverse_schema(schema['return_schema'], context)
        if 'json_schema_input_schema' in schema:
            traverse_schema(schema['json_schema_input_schema'], context)
    elif schema_type == 'function-wrap':
        # TODO duplicate schema types for serializers and validators, needs to be deduplicated.
        if 'return_schema' in schema:
            traverse_schema(schema['return_schema'], context)
        if 'schema' in schema:
            traverse_schema(schema['schema'], context)
        if 'json_schema_input_schema' in schema:
            traverse_schema(schema['json_schema_input_schema'], context)
    else:
        if 'schema' in schema:
            traverse_schema(schema['schema'], context)

    if 'serialization' in schema:
        traverse_schema(schema['serialization'], context)
    traverse_metadata(schema, context)

