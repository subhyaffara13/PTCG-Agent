
def require_deepspeed(test_case):
    """
    Decorator marking a test that requires deepspeed
    """
    return unittest.skipUnless(is_deepspeed_available(), "test requires deepspeed")(test_case)

