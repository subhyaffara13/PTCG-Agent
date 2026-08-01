
def require_vptq(test_case):
    """
    Decorator marking a test that requires vptq
    """
    return unittest.skipUnless(is_vptq_available(), "test requires vptq")(test_case)

