
def require_natten(test_case):
    """
    Decorator marking a test that requires NATTEN.

    These tests are skipped when NATTEN isn't installed.

    """
    return unittest.skipUnless(is_natten_available(), "test requires natten")(test_case)

