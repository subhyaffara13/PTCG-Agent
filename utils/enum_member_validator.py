
def enum_member_validator(v: Any, field: 'ModelField', config: 'BaseConfig') -> Enum:
    try:
        enum_v = field.type_(v)
    except ValueError:
        # field.type_ should be an enum, so will be iterable
        raise errors.EnumMemberError(enum_values=list(field.type_))
    return enum_v.value if config.use_enum_values else enum_v

