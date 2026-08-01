
def constr_strip_whitespace(v: 'StrBytes', field: 'ModelField', config: 'BaseConfig') -> 'StrBytes':
    strip_whitespace = field.type_.strip_whitespace or config.anystr_strip_whitespace
    if strip_whitespace:
        v = v.strip()

    return v

