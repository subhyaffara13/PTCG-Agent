
def require_torch_multi_npu(test_case):
    """
    Decorator marking a test that requires a multi-NPU setup (in PyTorch). These tests are skipped on a machine without
    multiple NPUs.

    To run *only* the multi_npu tests, assuming all test names contain multi_npu: $ pytest -sv ./tests -k "multi_npu"
    """
    if not is_torch_npu_available():
        return unittest.skip(reason="test requires PyTorch NPU")(test_case)

    return unittest.skipUnless(torch.npu.device_count() > 1, "test requires multiple NPUs")(test_case)

