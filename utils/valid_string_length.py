
def valid_string_length(domain: Union[bytes, str], trailing_dot: bool) -> bool:
    """Check that a full domain name does not exceed the maximum length.

    Per :rfc:`1035`, a domain name is limited to 253 octets when no trailing
    dot is present, or 254 octets when one is included.

    :param domain: The full (possibly multi-label) domain name.
    :param trailing_dot: ``True`` if ``domain`` includes a trailing ``.``.
    :returns: ``True`` if the domain is within the length limit, otherwise
        ``False``.
    """
    return len(domain) <= (254 if trailing_dot else 253)


def valid_string_length(label: Union[bytes, str], trailing_dot: bool) -> bool:
    if len(label) > (254 if trailing_dot else 253):
        return False
    return True

