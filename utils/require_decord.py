
def require_decord(test_case):
    """
    Decorator marking a test that requires decord
    """
    return unittest.skipUnless(is_decord_available(), "test requires decord")(test_case)

