
def test_sigint(env, target, kwargs):
    backend = env.get("MPLBACKEND")
    if not backend.startswith(("qt", "macosx")):
        pytest.skip("SIGINT currently only tested on qt and macosx")
    source = (inspect.getsource(_test_sigint_impl) +
              f"\n_test_sigint_impl({backend!r}, {target!r}, {kwargs!r})")
    with _WaitForStringPopen([sys.executable, "-c", source]) as proc:
        try:
            proc.wait_for('DRAW')
            stdout, _ = proc.communicate(timeout=_test_timeout)
        except Exception:
            proc.kill()
            stdout, _ = proc.communicate()
            raise
        assert 'SUCCESS' in stdout

