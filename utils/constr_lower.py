
def constr_lower(v: 'StrBytes', field: 'ModelField', config: 'BaseConfig') -> 'StrBytes':
    lower = field.type_.to_lower or config.anystr_lower
    if lower:
        v = v.lower()
    return v

