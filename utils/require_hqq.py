
def require_hqq(test_case):
    """
    Decorator for hqq dependency
    """
    return unittest.skipUnless(is_hqq_available(), "test requires hqq")(test_case)

