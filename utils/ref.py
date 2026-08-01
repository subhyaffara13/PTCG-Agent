
def ref(validator, ref, instance, schema):
    yield from validator._validate_reference(ref=ref, instance=instance)

