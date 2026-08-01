
def require_torch_multi_xpu(test_case):
    """
    Decorator marking a test that requires a multi-XPU setup (in PyTorch). These tests are skipped on a machine without
    multiple XPUs.

    To run *only* the multi_xpu tests, assuming all test names contain multi_xpu: $ pytest -sv ./tests -k "multi_xpu"
    """
    if not is_torch_xpu_available():
        return unittest.skip(reason="test requires PyTorch XPU")(test_case)

    return unittest.skipUnless(torch.xpu.device_count() > 1, "test requires multiple XPUs")(test_case)

