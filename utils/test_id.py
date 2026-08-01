
def test_id(id_val):
    """Test function identifier

    Use this decorator before a test function indicates its simple ID
    """

    def _has_id(func):
        if not hasattr(func, "_test_id"):
            func._test_id = id_val
        return func

    return _has_id

