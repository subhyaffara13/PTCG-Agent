
def require_causal_conv1d(test_case):
    """
    Decorator marking a test that requires causal-conv1d.

    These tests are skipped when causal-conv1d isn't installed.
    """

    return unittest.skipUnless(
        is_causal_conv1d_available(),
        "test requires `causal-conv1d`",
    )(test_case)

