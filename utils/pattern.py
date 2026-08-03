import re

def pattern(validator, patrn, instance, schema):
    if (
        validator.is_type(instance, "string")
        and not re.search(patrn, instance)
    ):
        yield ValidationError(f"{instance!r} does not match {patrn!r}")

