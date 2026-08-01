
def constr_length_validator(v: 'StrBytes', field: 'ModelField', config: 'BaseConfig') -> 'StrBytes':
    v_len = len(v)

    min_length = field.type_.min_length if field.type_.min_length is not None else config.min_anystr_length
    if v_len < min_length:
        raise errors.AnyStrMinLengthError(limit_value=min_length)

    max_length = field.type_.max_length if field.type_.max_length is not None else config.max_anystr_length
    if max_length is not None and v_len > max_length:
        raise errors.AnyStrMaxLengthError(limit_value=max_length)

    return v

