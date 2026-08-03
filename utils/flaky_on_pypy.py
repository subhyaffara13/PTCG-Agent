import functools

def flaky_on_pypy(func):
    @functools.wraps(func)
    def _func():
        try:
            func()
        except AssertionError:  # pragma: no cover
            if IS_PYPY:
                msg = "Flaky monkeypatch on PyPy (#4124)"
                pytest.xfail(f"{msg}. Original discussion in #3707, #3709.")
            raise

    return _func

