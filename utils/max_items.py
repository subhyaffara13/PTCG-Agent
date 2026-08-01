
def maxItems(validator, mI, instance, schema):
    if validator.is_type(instance, "array") and len(instance) > mI:
        message = "is expected to be empty" if mI == 0 else "is too long"
        yield ValidationError(f"{instance!r} {message}")

