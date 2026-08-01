
def require_qutlass(test_case):
    """
    Decorator marking a test that requires qutlass
    """
    return unittest.skipUnless(is_qutlass_available(), "test requires qutlass")(test_case)

