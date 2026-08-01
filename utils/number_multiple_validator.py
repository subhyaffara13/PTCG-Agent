
def number_multiple_validator(v: 'Number', field: 'ModelField') -> 'Number':
    field_type: ConstrainedNumber = field.type_
    if field_type.multiple_of is not None:
        mod = float(v) / float(field_type.multiple_of) % 1
        if not almost_equal_floats(mod, 0.0) and not almost_equal_floats(mod, 1.0):
            raise errors.NumberNotMultipleError(multiple_of=field_type.multiple_of)
    return v

