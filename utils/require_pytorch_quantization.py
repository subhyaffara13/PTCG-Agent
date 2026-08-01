
def require_pytorch_quantization(test_case):
    """
    Decorator marking a test that requires PyTorch Quantization Toolkit. These tests are skipped when PyTorch
    Quantization Toolkit isn't installed.
    """
    return unittest.skipUnless(is_pytorch_quantization_available(), "test requires PyTorch Quantization Toolkit")(
        test_case
    )

