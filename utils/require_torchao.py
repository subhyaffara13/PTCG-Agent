
def require_torchao(test_case):
    """Decorator marking a test that requires torchao"""
    return unittest.skipUnless(is_torchao_available(), "test requires torchao")(test_case)

