
def ip_v6_address_validator(v: Any) -> IPv6Address:
    if isinstance(v, IPv6Address):
        return v

    try:
        return IPv6Address(v)
    except ValueError:
        raise errors.IPv6AddressError()


def ip_v6_address_validator(input_value: Any, /) -> IPv6Address:
    if isinstance(input_value, IPv6Address):
        return input_value

    try:
        return IPv6Address(input_value)
    except ValueError:
        raise PydanticCustomError('ip_v6_address', 'Input is not a valid IPv6 address')

