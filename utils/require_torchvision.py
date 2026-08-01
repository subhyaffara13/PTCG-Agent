
def require_torchvision(test_case):
    """
    Decorator marking a test that requires Torchvision.

    These tests are skipped when Torchvision isn't installed.

    """
    return unittest.skipUnless(is_torchvision_available(), "test requires Torchvision")(test_case)

