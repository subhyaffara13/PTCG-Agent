
def require_huggingface_hub_greater_or_equal(version: str):
    """
    Decorator marking a test that requires huggingface_hub version >= `version`.

    These tests are skipped when huggingface_hub version is less than `version`.
    """

    def decorator(test_case):
        return unittest.skipUnless(
            is_huggingface_hub_greater_or_equal(version), f"test requires huggingface_hub version >= {version}"
        )(test_case)

    return decorator

