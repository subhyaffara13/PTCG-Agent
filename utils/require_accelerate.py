
def require_accelerate(test_case, min_version: str = ACCELERATE_MIN_VERSION):
    """
    Decorator marking a test that requires accelerate. These tests are skipped when accelerate isn't installed.
    """
    return unittest.skipUnless(
        is_accelerate_available(min_version), f"test requires accelerate version >= {min_version}"
    )(test_case)

