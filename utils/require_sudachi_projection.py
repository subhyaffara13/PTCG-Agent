
def require_sudachi_projection(test_case):
    """
    Decorator marking a test that requires sudachi_projection
    """
    return unittest.skipUnless(is_sudachi_projection_available(), "test requires sudachi which supports projection")(
        test_case
    )

