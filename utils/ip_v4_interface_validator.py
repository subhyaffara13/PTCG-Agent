
def ip_v4_interface_validator(v: Any) -> IPv4Interface:
    if isinstance(v, IPv4Interface):
        return v

    try:
        return IPv4Interface(v)
    except ValueError:
        raise errors.IPv4InterfaceError()


def ip_v4_interface_validator(input_value: Any, /) -> IPv4Interface:
    if isinstance(input_value, IPv4Interface):
        return input_value

    try:
        return IPv4Interface(input_value)
    except ValueError:
        raise PydanticCustomError('ip_v4_interface', 'Input is not a valid IPv4 interface')

