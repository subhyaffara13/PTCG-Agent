
def _validator_for_name(validator_name):
    if validator_name not in VALIDATORS:
        msg = f"Invalid validator '{validator_name}' value!\nValid values are: {VALIDATORS}"
        raise ValueError(msg)

    for name, module, validator_cls in _VALIDATOR_MAP:
        if module and validator_name == name:
            return validator_cls
    # we always return something.
    msg = f"Missing validator for {validator_name!r}"
    raise ValueError(msg)

