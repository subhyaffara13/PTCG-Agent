
def contains_draft6_draft7(validator, contains, instance, schema):
    if not validator.is_type(instance, "array"):
        return

    if not any(
        validator.evolve(schema=contains).is_valid(element)
        for element in instance
    ):
        yield ValidationError(
            f"None of {instance!r} are valid under the given schema",
        )

