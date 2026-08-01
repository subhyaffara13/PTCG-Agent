
def allOf(validator, allOf, instance, schema):
    for index, subschema in enumerate(allOf):
        yield from validator.descend(instance, subschema, schema_path=index)

