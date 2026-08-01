
def require_torch_mps(test_case):
    """Decorator marking a test that requires CUDA and PyTorch."""
    return unittest.skipUnless(torch_device == "mps", "test requires MPS")(test_case)

