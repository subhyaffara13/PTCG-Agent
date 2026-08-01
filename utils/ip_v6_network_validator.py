
def ip_v6_network_validator(v: Any) -> IPv6Network:
    """
    Assume IPv6Network initialised with a default ``strict`` argument

    See more:
    https://docs.python.org/library/ipaddress.html#ipaddress.IPv6Network
    """
    if isinstance(v, IPv6Network):
        return v

    try:
        return IPv6Network(v)
    except ValueError:
        raise errors.IPv6NetworkError()


def ip_v6_network_validator(input_value: Any, /) -> IPv6Network:
    """Assume IPv6Network initialised with a default `strict` argument.

    See more:
    https://docs.python.org/library/ipaddress.html#ipaddress.IPv6Network
    """
    if isinstance(input_value, IPv6Network):
        return input_value

    try:
        return IPv6Network(input_value)
    except ValueError:
        raise PydanticCustomError('ip_v6_network', 'Input is not a valid IPv6 network')

