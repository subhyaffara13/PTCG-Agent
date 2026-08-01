
def require_quark(test_case):
    """
    Decorator for quark dependency
    """
    return unittest.skipUnless(is_quark_available(), "test requires quark")(test_case)

