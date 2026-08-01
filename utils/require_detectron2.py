
def require_detectron2(test_case):
    """Decorator marking a test that requires detectron2."""
    return unittest.skipUnless(is_detectron2_available(), "test requires `detectron2`")(test_case)

