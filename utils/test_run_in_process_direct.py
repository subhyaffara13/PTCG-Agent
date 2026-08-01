
def test_run_in_process_direct(test_fn):
    """Makes sure there is no GIL deadlock when using processes.

    This test is for completion, but it was never an issue.
    """
    assert _run_in_process(test_fn) == 0

