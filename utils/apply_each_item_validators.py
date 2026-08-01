
def apply_each_item_validators(
    schema: core_schema.CoreSchema,
    each_item_validators: list[Decorator[ValidatorDecoratorInfo]],
) -> core_schema.CoreSchema:
    # This V1 compatibility shim should eventually be removed

    # fail early if each_item_validators is empty
    if not each_item_validators:
        return schema

    # push down any `each_item=True` validators
    # note that this won't work for any Annotated types that get wrapped by a function validator
    # but that's okay because that didn't exist in V1
    if schema['type'] == 'nullable':
        schema['schema'] = apply_each_item_validators(schema['schema'], each_item_validators)
        return schema
    elif schema['type'] == 'tuple':
        if (variadic_item_index := schema.get('variadic_item_index')) is not None:
            schema['items_schema'][variadic_item_index] = apply_validators(
                schema['items_schema'][variadic_item_index],
                each_item_validators,
            )
    elif is_list_like_schema_with_items_schema(schema):
        inner_schema = schema.get('items_schema', core_schema.any_schema())
        schema['items_schema'] = apply_validators(inner_schema, each_item_validators)
    elif schema['type'] == 'dict':
        inner_schema = schema.get('values_schema', core_schema.any_schema())
        schema['values_schema'] = apply_validators(inner_schema, each_item_validators)
    else:
        raise TypeError(
            f'`@validator(..., each_item=True)` cannot be applied to fields with a schema of {schema["type"]}'
        )
    return schema

