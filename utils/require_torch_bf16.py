
def require_torch_bf16(test_case):
    """Decorator marking a test that requires a device that supports bf16"""
    return unittest.skipUnless(
        is_torch_bf16_available_on_device(torch_device), "test requires device with bf16 support"
    )(test_case)

