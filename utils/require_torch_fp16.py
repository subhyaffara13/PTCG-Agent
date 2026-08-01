
def require_torch_fp16(test_case):
    """Decorator marking a test that requires a device that supports fp16"""
    return unittest.skipUnless(
        is_torch_fp16_available_on_device(torch_device), "test requires device with fp16 support"
    )(test_case)

