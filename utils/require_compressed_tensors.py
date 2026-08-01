
def require_compressed_tensors(test_case):
    """
    Decorator for compressed_tensors dependency
    """
    return unittest.skipUnless(is_compressed_tensors_available(), "test requires compressed_tensors")(test_case)

