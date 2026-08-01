
def minLength(validator, mL, instance, schema):
    if validator.is_type(instance, "string") and len(instance) < mL:
        message = "should be non-empty" if mL == 1 else "is too short"
        yield ValidationError(f"{instance!r} {message}")

