
def require_mistral_common(test_case):
    """
    Decorator marking a test that requires mistral-common. These tests are skipped when mistral-common isn't available.
    """
    return unittest.skipUnless(is_mistral_common_available(), "test requires mistral-common")(test_case)

