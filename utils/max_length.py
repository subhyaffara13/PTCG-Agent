
def maxLength(validator, mL, instance, schema):
    if validator.is_type(instance, "string") and len(instance) > mL:
        message = "is expected to be empty" if mL == 0 else "is too long"
        yield ValidationError(f"{instance!r} {message}")

