
def require_swanlab(test_case):
    """
    Decorator marking a test that requires swanlab.

    These tests are skipped when swanlab isn't installed.

    """
    return unittest.skipUnless(is_swanlab_available(), "test requires swanlab")(test_case)

