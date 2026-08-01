
def prep_validators(v_funcs: Iterable[AnyCallable]) -> 'ValidatorsList':
    return [make_generic_validator(f) for f in v_funcs if f]

