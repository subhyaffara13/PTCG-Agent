
def require_apollo_torch(test_case):
    """
    Decorator marking a test that requires GaLore. These tests are skipped when APOLLO isn't installed.
    https://github.com/zhuhanqing/APOLLO
    """
    return unittest.skipUnless(is_apollo_torch_available(), "test requires APOLLO")(test_case)

