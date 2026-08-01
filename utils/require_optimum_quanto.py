
def require_optimum_quanto(test_case):
    """
    Decorator for quanto dependency
    """
    return unittest.skipUnless(is_optimum_quanto_available(), "test requires optimum-quanto")(test_case)

