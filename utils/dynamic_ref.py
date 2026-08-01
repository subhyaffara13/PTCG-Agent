
def dynamicRef(validator, dynamicRef, instance, schema):
    yield from validator._validate_reference(ref=dynamicRef, instance=instance)

