
def require_spqr(test_case):
    """
    Decorator marking a test that requires spqr
    """
    return unittest.skipUnless(is_spqr_available(), "test requires spqr")(test_case)

