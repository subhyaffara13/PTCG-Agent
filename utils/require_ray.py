
def require_ray(test_case):
    """
    Decorator marking a test that requires Ray/tune.

    These tests are skipped when Ray/tune isn't installed.

    """
    return unittest.skipUnless(is_ray_available(), "test requires Ray/tune")(test_case)

