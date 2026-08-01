
def require_torch_accelerator(test_case):
    """Decorator marking a test that requires an accessible accelerator and PyTorch."""
    return unittest.skipUnless(torch_device is not None and torch_device != "cpu", "test requires accelerator")(
        test_case
    )

