
def number_size_validator(v: 'Number', field: 'ModelField') -> 'Number':
    field_type: ConstrainedNumber = field.type_
    if field_type.gt is not None and not v > field_type.gt:
        raise errors.NumberNotGtError(limit_value=field_type.gt)
    elif field_type.ge is not None and not v >= field_type.ge:
        raise errors.NumberNotGeError(limit_value=field_type.ge)

    if field_type.lt is not None and not v < field_type.lt:
        raise errors.NumberNotLtError(limit_value=field_type.lt)
    if field_type.le is not None and not v <= field_type.le:
        raise errors.NumberNotLeError(limit_value=field_type.le)

    return v

