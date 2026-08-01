
def disallow_draft3(validator, disallow, instance, schema):
    for disallowed in _utils.ensure_list(disallow):
        if validator.evolve(schema={"type": [disallowed]}).is_valid(instance):
            message = f"{disallowed!r} is disallowed for {instance!r}"
            yield ValidationError(message)

