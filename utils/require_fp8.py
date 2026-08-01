
def require_fp8(test_case):
    """Decorator marking a test that requires supports for fp8"""
    return unittest.skipUnless(is_accelerate_available() and is_fp8_available(), "test requires fp8 support")(
        test_case
    )

