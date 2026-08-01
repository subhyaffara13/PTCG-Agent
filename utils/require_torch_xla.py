
def require_torch_xla(test_case):
    """
    Decorator marking a test that requires TorchXLA (in PyTorch).
    """
    return unittest.skipUnless(is_torch_xla_available(), "test requires TorchXLA")(test_case)

