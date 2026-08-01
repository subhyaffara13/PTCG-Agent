
def float_finite_validator(v: 'Number', field: 'ModelField', config: 'BaseConfig') -> 'Number':
    allow_inf_nan = getattr(field.type_, 'allow_inf_nan', None)
    if allow_inf_nan is None:
        allow_inf_nan = config.allow_inf_nan

    if allow_inf_nan is False and (math.isnan(v) or math.isinf(v)):
        raise errors.NumberNotFiniteError()
    return v

