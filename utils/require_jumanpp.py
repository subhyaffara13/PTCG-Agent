
def require_jumanpp(test_case):
    """
    Decorator marking a test that requires jumanpp
    """
    return unittest.skipUnless(is_jumanpp_available(), "test requires jumanpp")(test_case)

