
def test_run_in_process_multiple_threads_sequential(test_fn):
    """Makes sure there is no GIL deadlock when running in a thread multiple times sequentially.

    It runs in a separate process to be able to stop and assert if it deadlocks.
    """
    assert _run_in_process(_run_in_threads, test_fn, num_threads=8, parallel=False) == 0

