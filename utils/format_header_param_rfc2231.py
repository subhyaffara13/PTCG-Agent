
def format_header_param_rfc2231(name: str, value: _TYPE_FIELD_VALUE) -> str:
    """
    Helper function to format and quote a single header parameter using the
    strategy defined in RFC 2231.

    Particularly useful for header parameters which might contain
    non-ASCII values, like file names. This follows
    `RFC 2388 Section 4.4 <https://tools.ietf.org/html/rfc2388#section-4.4>`_.

    :param name:
        The name of the parameter, a string expected to be ASCII only.
    :param value:
        The value of the parameter, provided as ``bytes`` or `str``.
    :returns:
        An RFC-2231-formatted unicode string.

    .. deprecated:: 2.0.0
        Will be removed in urllib3 v3.0. This is not valid for
        ``multipart/form-data`` header parameters.
    """
    import warnings

    warnings.warn(
        "'format_header_param_rfc2231' is insecure, deprecated and will be "
        "removed in urllib3 v3.0. This is not valid for "
        "multipart/form-data header parameters.",
        FutureWarning,
        stacklevel=2,
    )

    if isinstance(value, bytes):
        value = value.decode("utf-8")

    if not any(ch in value for ch in '"\\\r\n'):
        result = f'{name}="{value}"'
        try:
            result.encode("ascii")
        except (UnicodeEncodeError, UnicodeDecodeError):
            pass
        else:
            return result

    value = email.utils.encode_rfc2231(value, "utf-8")
    value = f"{name}*={value}"

    return value


def format_header_param_rfc2231(name: str, value: _TYPE_FIELD_VALUE) -> str:
    """
    Helper function to format and quote a single header parameter using the
    strategy defined in RFC 2231.

    Particularly useful for header parameters which might contain
    non-ASCII values, like file names. This follows
    `RFC 2388 Section 4.4 <https://tools.ietf.org/html/rfc2388#section-4.4>`_.

    :param name:
        The name of the parameter, a string expected to be ASCII only.
    :param value:
        The value of the parameter, provided as ``bytes`` or `str``.
    :returns:
        An RFC-2231-formatted unicode string.

    .. deprecated:: 2.0.0
        Will be removed in urllib3 v2.1.0. This is not valid for
        ``multipart/form-data`` header parameters.
    """
    import warnings

    warnings.warn(
        "'format_header_param_rfc2231' is deprecated and will be "
        "removed in urllib3 v2.1.0. This is not valid for "
        "multipart/form-data header parameters.",
        DeprecationWarning,
        stacklevel=2,
    )

    if isinstance(value, bytes):
        value = value.decode("utf-8")

    if not any(ch in value for ch in '"\\\r\n'):
        result = f'{name}="{value}"'
        try:
            result.encode("ascii")
        except (UnicodeEncodeError, UnicodeDecodeError):
            pass
        else:
            return result

    value = email.utils.encode_rfc2231(value, "utf-8")
    value = f"{name}*={value}"

    return value

