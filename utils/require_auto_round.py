
def require_auto_round(test_case):
    """
    Decorator for auto_round dependency
    """
    return unittest.skipUnless(is_auto_round_available(), "test requires autoround")(test_case)

