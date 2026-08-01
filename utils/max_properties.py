
def maxProperties(validator, mP, instance, schema):
    if not validator.is_type(instance, "object"):
        return
    if validator.is_type(instance, "object") and len(instance) > mP:
        message = (
            "is expected to be empty" if mP == 0
            else "has too many properties"
        )
        yield ValidationError(f"{instance!r} {message}")

