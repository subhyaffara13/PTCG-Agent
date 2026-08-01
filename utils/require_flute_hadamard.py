
def require_flute_hadamard(test_case):
    """
    Decorator marking a test that requires higgs and hadamard
    """
    return unittest.skipUnless(
        is_flute_available() and is_hadamard_available(), "test requires flute and fast_hadamard_transform"
    )(test_case)

