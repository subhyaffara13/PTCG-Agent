
def require_torch_xpu(test_case):
    """
    Decorator marking a test that requires XPU (in PyTorch).

    These tests are skipped when XPU backend is not available.
    """
    return unittest.skipUnless(is_torch_xpu_available(), "test requires XPU device")(test_case)

