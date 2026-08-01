
def _inject_headers(name, scheme):
    """
    Given a scheme name and the resolved scheme,
    if the scheme does not include headers, resolve
    the fallback scheme for the name and use headers
    from it. pypa/distutils#88
    """
    # Bypass the preferred scheme, which may not
    # have defined headers.
    fallback = _load_scheme(name)
    scheme.setdefault('headers', fallback['headers'])
    return scheme

