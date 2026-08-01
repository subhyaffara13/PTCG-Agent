
def require_non_hpu(test_case):
    """
    Decorator marking a test that should be skipped for HPU.
    """
    return unittest.skipUnless(torch_device != "hpu", "test requires a non-HPU")(test_case)

