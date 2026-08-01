
def test_min_module_version_python3_basestring_error():
    with warns(UserWarning):
        import_module('mpmath', min_module_version='1000.0.1')

