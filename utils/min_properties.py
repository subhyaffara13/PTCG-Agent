
def minProperties(validator, mP, instance, schema):
    if validator.is_type(instance, "object") and len(instance) < mP:
        message = (
            "should be non-empty" if mP == 1
            else "does not have enough properties"
        )
        yield ValidationError(f"{instance!r} {message}")

