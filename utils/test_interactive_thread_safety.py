
def test_interactive_thread_safety(env):
    proc = _run_helper(_test_thread_impl, timeout=_test_timeout, extra_env=env)
    assert proc.stdout.count("CloseEvent") == 1

