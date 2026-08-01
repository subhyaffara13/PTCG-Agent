
def require_torch_npu(test_case):
    """
    Decorator marking a test that requires NPU (in PyTorch).
    """
    return unittest.skipUnless(is_torch_npu_available(), "test requires PyTorch NPU")(test_case)

