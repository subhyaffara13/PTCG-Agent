
def constr_upper(v: 'StrBytes', field: 'ModelField', config: 'BaseConfig') -> 'StrBytes':
    upper = field.type_.to_upper or config.anystr_upper
    if upper:
        v = v.upper()

    return v

