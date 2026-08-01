
def properties_draft3(validator, properties, instance, schema):
    if not validator.is_type(instance, "object"):
        return

    for property, subschema in properties.items():
        if property in instance:
            yield from validator.descend(
                instance[property],
                subschema,
                path=property,
                schema_path=property,
            )
        elif subschema.get("required", False):
            error = ValidationError(f"{property!r} is a required property")
            error._set(
                validator="required",
                validator_value=subschema["required"],
                instance=instance,
                schema=schema,
            )
            error.path.appendleft(property)
            error.schema_path.extend([property, "required"])
            yield error

