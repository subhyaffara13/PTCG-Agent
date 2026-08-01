
def suppress_matplotlib_deprecation_warning():
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", MatplotlibDeprecationWarning)
        yield

