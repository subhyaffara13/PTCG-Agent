
def ip_v4_address_validator(v: Any) -> IPv4Address:
    if isinstance(v, IPv4Address):
        return v

    try:
        return IPv4Address(v)
    except ValueError:
        raise errors.IPv4AddressError()


def ip_v4_address_validator(input_value: Any, /) -> IPv4Address:
    if isinstance(input_value, IPv4Address):
        return input_value

    try:
        return IPv4Address(input_value)
    except ValueError:
        raise PydanticCustomError('ip_v4_address', 'Input is not a valid IPv4 address')

