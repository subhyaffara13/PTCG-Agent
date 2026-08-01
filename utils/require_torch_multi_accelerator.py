
def require_torch_multi_accelerator(test_case):
    """
    Decorator marking a test that requires a multi-accelerator (in PyTorch). These tests are skipped on a machine
    without multiple accelerators. To run *only* the multi_accelerator tests, assuming all test names contain
    multi_accelerator: $ pytest -sv ./tests -k "multi_accelerator"
    """
    if not is_torch_available():
        return unittest.skip(reason="test requires PyTorch")(test_case)

    return unittest.skipUnless(backend_device_count(torch_device) > 1, "test requires multiple accelerators")(
        test_case
    )

