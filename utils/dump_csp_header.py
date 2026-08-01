
def dump_csp_header(header: ds.ContentSecurityPolicy) -> str:
    """Dump a Content Security Policy header.

    These are structured into policies such as "default-src 'self';
    script-src 'self'".

    .. versionadded:: 1.0.0
       Support for Content Security Policy headers was added.

    """
    return "; ".join(f"{key} {value}" for key, value in header.items())

