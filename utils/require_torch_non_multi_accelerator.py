
def require_torch_non_multi_accelerator(test_case):
    """
    Decorator marking a test that requires 0 or 1 accelerator setup (in PyTorch).
    """
    if not is_torch_available():
        return unittest.skip(reason="test requires PyTorch")(test_case)

    return unittest.skipUnless(backend_device_count(torch_device) < 2, "test requires 0 or 1 accelerator")(test_case)

