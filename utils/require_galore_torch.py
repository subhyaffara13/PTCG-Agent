
def require_galore_torch(test_case):
    """
    Decorator marking a test that requires GaLore. These tests are skipped when GaLore isn't installed.
    https://github.com/jiaweizzhao/GaLore
    """
    return unittest.skipUnless(is_galore_torch_available(), "test requires GaLore")(test_case)

