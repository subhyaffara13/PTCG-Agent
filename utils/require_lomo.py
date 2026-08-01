
def require_lomo(test_case):
    """
    Decorator marking a test that requires LOMO. These tests are skipped when LOMO-optim isn't installed.
    https://github.com/OpenLMLab/LOMO
    """
    return unittest.skipUnless(is_lomo_available(), "test requires LOMO")(test_case)

