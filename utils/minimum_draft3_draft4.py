
def minimum_draft3_draft4(validator, minimum, instance, schema):
    if not validator.is_type(instance, "number"):
        return

    if schema.get("exclusiveMinimum", False):
        failed = instance <= minimum
        cmp = "less than or equal to"
    else:
        failed = instance < minimum
        cmp = "less than"

    if failed:
        message = f"{instance!r} is {cmp} the minimum of {minimum!r}"
        yield ValidationError(message)

