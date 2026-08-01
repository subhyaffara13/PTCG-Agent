
def require_optimum(test_case):
    """
    Decorator for optimum dependency
    """
    return unittest.skipUnless(is_optimum_available(), "test requires optimum")(test_case)

