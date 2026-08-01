
def require_openai(test_case):
    """
    Decorator marking a test that requires openai
    """
    return unittest.skipUnless(is_openai_available(), "test requires openai")(test_case)

