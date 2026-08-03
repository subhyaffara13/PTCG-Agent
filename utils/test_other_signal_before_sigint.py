import os
import sys

def test_other_signal_before_sigint(env, target, kwargs, request):
    backend = env.get("MPLBACKEND")
    if not backend.startswith(("qt", "macosx")):
        pytest.skip("SIGINT currently only tested on qt and macosx")
    if backend == "macosx":
        request.node.add_marker(pytest.mark.xfail(reason="macosx backend is buggy"))
    if sys.platform == "darwin" and target == "show":
        # We've not previously had these toolkits installed on CI, and so were never
        # aware that this was crashing. However, we've had little luck reproducing it
        # locally, so mark it xfail for now. For more information, see
        # https://github.com/matplotlib/matplotlib/issues/27984
        request.node.add_marker(
            pytest.mark.xfail(reason="Qt backend is buggy on macOS"))
    source = (inspect.getsource(_test_other_signal_before_sigint_impl) +
              "\n_test_other_signal_before_sigint_impl("
              f"{backend!r}, {target!r}, {kwargs!r})")
    with _WaitForStringPopen([sys.executable, "-c", source]) as proc:
        try:
            proc.wait_for('DRAW')
            os.kill(proc.pid, signal.SIGUSR1)
            proc.wait_for('SIGUSR1')
            os.kill(proc.pid, signal.SIGINT)
            stdout, _ = proc.communicate(timeout=_test_timeout)
        except Exception:
            proc.kill()
            stdout, _ = proc.communicate()
            raise
    print(stdout)
    assert 'SUCCESS' in stdout

