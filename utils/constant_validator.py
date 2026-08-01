
def constant_validator(v: 'Any', field: 'ModelField') -> 'Any':
    """Validate ``const`` fields.

    The value provided for a ``const`` field must be equal to the default value
    of the field. This is to support the keyword of the same name in JSON
    Schema.
    """
    if v != field.default:
        raise errors.WrongConstantError(given=v, permitted=[field.default])

    return v

