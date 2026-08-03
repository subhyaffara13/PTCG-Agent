from typing import Any

def ip_v6_interface_validator(v: Any) -> IPv6Interface:
    if isinstance(v, IPv6Interface):
        return v

    try:
        return IPv6Interface(v)
    except ValueError:
        raise errors.IPv6InterfaceError()


def ip_v6_interface_validator(input_value: Any, /) -> IPv6Interface:
    if isinstance(input_value, IPv6Interface):
        return input_value

    try:
        return IPv6Interface(input_value)
    except ValueError:
        raise PydanticCustomError('ip_v6_interface', 'Input is not a valid IPv6 interface')

