
def exclusiveMaximum(validator, maximum, instance, schema):
    if not validator.is_type(instance, "number"):
        return

    if instance >= maximum:
        yield ValidationError(
            f"{instance!r} is greater than or equal "
            f"to the maximum of {maximum!r}",
        )

