import os

def test_interactive_timers(env):
    if env["MPLBACKEND"] == "gtk3cairo" and os.getenv("CI"):
        pytest.skip("gtk3cairo timers do not work in remote CI")
    if env["MPLBACKEND"] == "wx":
        pytest.skip("wx backend is deprecated; tests failed on appveyor")
    _run_helper(_impl_test_interactive_timers,
                timeout=_test_timeout, extra_env=env)

