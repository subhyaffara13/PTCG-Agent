
def test_create_figure_on_worker_thread_fails():
    subprocess_run_helper(
        _test_create_figure_on_worker_thread_fails,
        timeout=_test_timeout,
        extra_env={"MPLBACKEND": "macosx"}
    )

