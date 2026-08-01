
def require_av(test_case):
    """
    Decorator marking a test that requires av
    """
    return unittest.skipUnless(is_av_available(), "test requires av")(test_case)

