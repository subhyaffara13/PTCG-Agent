
def require_torch_greater_or_equal(version: str):
    """
    Decorator marking a test that requires PyTorch version >= `version`.

    These tests are skipped when PyTorch version is less than `version`.
    """

    def decorator(test_case):
        return unittest.skipUnless(is_torch_greater_or_equal(version), f"test requires PyTorch version >= {version}")(
            test_case
        )

    return decorator

