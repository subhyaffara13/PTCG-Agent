
def require_torch_multi_hpu(test_case):
    """
    Decorator marking a test that requires a multi-HPU setup (in PyTorch). These tests are skipped on a machine without
    multiple HPUs.

    To run *only* the multi_hpu tests, assuming all test names contain multi_hpu: $ pytest -sv ./tests -k "multi_hpu"
    """
    if not is_torch_hpu_available():
        return unittest.skip(reason="test requires PyTorch HPU")(test_case)

    return unittest.skipUnless(torch.hpu.device_count() > 1, "test requires multiple HPUs")(test_case)

