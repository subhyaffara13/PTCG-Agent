
def format_header_param_html5(name: str, value: _TYPE_FIELD_VALUE) -> str:
    """
    .. deprecated:: 2.0.0
        Renamed to :func:`format_multipart_header_param`. Will be
        removed in urllib3 v3.0.
    """
    import warnings

    warnings.warn(
        "'format_header_param_html5' has been renamed to "
        "'format_multipart_header_param'. The old name will be "
        "removed in urllib3 v3.0.",
        FutureWarning,
        stacklevel=2,
    )
    return format_multipart_header_param(name, value)


def format_header_param_html5(name: str, value: _TYPE_FIELD_VALUE) -> str:
    """
    .. deprecated:: 2.0.0
        Renamed to :func:`format_multipart_header_param`. Will be
        removed in urllib3 v2.1.0.
    """
    import warnings

    warnings.warn(
        "'format_header_param_html5' has been renamed to "
        "'format_multipart_header_param'. The old name will be "
        "removed in urllib3 v2.1.0.",
        DeprecationWarning,
        stacklevel=2,
    )
    return format_multipart_header_param(name, value)

