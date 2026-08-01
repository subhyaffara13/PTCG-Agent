
def test_lazy_linux_headless(env):
    proc = _run_helper(
        _lazy_headless,
        env.pop('MPLBACKEND'), env.pop("BACKEND_DEPS"),
        timeout=_test_timeout,
        extra_env={**env, 'DISPLAY': '', 'WAYLAND_DISPLAY': ''}
    )

