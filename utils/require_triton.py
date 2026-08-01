
def require_triton(min_version: str = TRITON_MIN_VERSION):
    """
    Decorator marking a test that requires triton. These tests are skipped when triton isn't installed.
    """

    def decorator(test_case):
        return unittest.skipUnless(is_triton_available(min_version), f"test requires triton version >= {min_version}")(
            test_case
        )

    return decorator

