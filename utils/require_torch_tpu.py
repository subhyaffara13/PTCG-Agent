
def require_torch_tpu(test_case):
    """
    Decorator marking a test that requires TPU (in PyTorch via torch_tpu).
    """
    return unittest.skipUnless(is_torch_tpu_available(), "test requires PyTorch TPU")(test_case)

