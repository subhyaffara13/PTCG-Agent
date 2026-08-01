
def extends_draft3(validator, extends, instance, schema):
    if validator.is_type(extends, "object"):
        yield from validator.descend(instance, extends)
        return
    for index, subschema in enumerate(extends):
        yield from validator.descend(instance, subschema, schema_path=index)

