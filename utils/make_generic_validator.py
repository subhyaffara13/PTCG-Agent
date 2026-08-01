
def make_generic_validator(validator: AnyCallable) -> 'ValidatorCallable':
    """
    Make a generic function which calls a validator with the right arguments.

    Unfortunately other approaches (eg. return a partial of a function that builds the arguments) is slow,
    hence this laborious way of doing things.

    It's done like this so validators don't all need **kwargs in their signature, eg. any combination of
    the arguments "values", "fields" and/or "config" are permitted.
    """
    from inspect import signature

    if not isinstance(validator, (partial, partialmethod)):
        # This should be the default case, so overhead is reduced
        sig = signature(validator)
        args = list(sig.parameters.keys())
    else:
        # Fix the generated argument lists of partial methods
        sig = signature(validator.func)
        args = [
            k
            for k in signature(validator.func).parameters.keys()
            if k not in validator.args | validator.keywords.keys()
        ]

    first_arg = args.pop(0)
    if first_arg == 'self':
        raise ConfigError(
            f'Invalid signature for validator {validator}: {sig}, "self" not permitted as first argument, '
            f'should be: (cls, value, values, config, field), "values", "config" and "field" are all optional.'
        )
    elif first_arg == 'cls':
        # assume the second argument is value
        return wraps(validator)(_generic_validator_cls(validator, sig, set(args[1:])))
    else:
        # assume the first argument was value which has already been removed
        return wraps(validator)(_generic_validator_basic(validator, sig, set(args)))

