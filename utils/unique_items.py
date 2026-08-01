
def uniqueItems(validator, uI, instance, schema):
    if (
        uI
        and validator.is_type(instance, "array")
        and not uniq(instance)
    ):
        yield ValidationError(f"{instance!r} has non-unique elements")

