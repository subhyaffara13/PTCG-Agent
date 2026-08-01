
def minItems(validator, mI, instance, schema):
    if validator.is_type(instance, "array") and len(instance) < mI:
        message = "should be non-empty" if mI == 1 else "is too short"
        yield ValidationError(f"{instance!r} {message}")

