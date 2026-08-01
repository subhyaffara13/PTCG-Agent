
def exclusiveMinimum(validator, minimum, instance, schema):
    if not validator.is_type(instance, "number"):
        return

    if instance <= minimum:
        yield ValidationError(
            f"{instance!r} is less than or equal to "
            f"the minimum of {minimum!r}",
        )

