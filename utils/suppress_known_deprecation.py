
def suppress_known_deprecation():
    with warnings.catch_warnings():
        warnings.filterwarnings('ignore', 'setup.py install is deprecated')
        yield


def suppress_known_deprecation():
    with warnings.catch_warnings(record=True) as ctx:
        warnings.filterwarnings(
            action='default',
            category=DeprecationWarning,
            message="distutils Version classes are deprecated.",
        )
        yield ctx

