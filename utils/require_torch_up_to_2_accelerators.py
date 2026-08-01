
def require_torch_up_to_2_accelerators(test_case):
    """
    Decorator marking a test that requires 0 or 1 or 2 accelerator setup (in PyTorch).
    """
    if not is_torch_available():
        return unittest.skip(reason="test requires PyTorch")(test_case)

    return unittest.skipUnless(backend_device_count(torch_device) < 3, "test requires 0 or 1 or 2 accelerators")(
        test_case
    )

