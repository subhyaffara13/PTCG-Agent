
def ip_v4_network_validator(v: Any) -> IPv4Network:
    """
    Assume IPv4Network initialised with a default ``strict`` argument

    See more:
    https://docs.python.org/library/ipaddress.html#ipaddress.IPv4Network
    """
    if isinstance(v, IPv4Network):
        return v

    try:
        return IPv4Network(v)
    except ValueError:
        raise errors.IPv4NetworkError()


def ip_v4_network_validator(input_value: Any, /) -> IPv4Network:
    """Assume IPv4Network initialised with a default `strict` argument.

    See more:
    https://docs.python.org/library/ipaddress.html#ipaddress.IPv4Network
    """
    if isinstance(input_value, IPv4Network):
        return input_value

    try:
        return IPv4Network(input_value)
    except ValueError:
        raise PydanticCustomError('ip_v4_network', 'Input is not a valid IPv4 network')

