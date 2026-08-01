
def require_fsdp(test_case, min_version: str = "1.12.0"):
    """
    Decorator marking a test that requires fsdp. These tests are skipped when fsdp isn't installed.
    """
    return unittest.skipUnless(is_fsdp_available(min_version), f"test requires torch version >= {min_version}")(
        test_case
    )

