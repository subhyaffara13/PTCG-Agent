
def const(validator, const, instance, schema):
    if not equal(instance, const):
        yield ValidationError(f"{const!r} was expected")

