
def test_cached_renderer():
    subprocess_run_helper(_test_cached_renderer, timeout=_test_timeout,
                          extra_env={"MPLBACKEND": "macosx"})

