
def require_torch_tensorrt_fx(test_case):
    """Decorator marking a test that requires Torch-TensorRT FX"""
    return unittest.skipUnless(is_torch_tensorrt_fx_available(), "test requires Torch-TensorRT FX")(test_case)

