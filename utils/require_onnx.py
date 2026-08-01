
def require_onnx(test_case):
    return unittest.skipUnless(is_onnx_available(), "test requires ONNX")(test_case)

