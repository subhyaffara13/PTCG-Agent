
def suppress_deprecation():
    with distutils.version.suppress_known_deprecation():
        yield

