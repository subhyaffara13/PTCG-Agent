from typing import Any, Callable

def _patch_unwrap_mock_aware() -> Generator[None]:
    """Context manager which replaces ``inspect.unwrap`` with a version
    that's aware of mock objects and doesn't recurse into them."""
    real_unwrap = inspect.unwrap

    def _mock_aware_unwrap(
        func: Callable[..., Any], *, stop: Callable[[Any], Any] | None = None
    ) -> Any:
        try:
            if stop is None or stop is _is_mocked:
                return real_unwrap(func, stop=_is_mocked)
            _stop = stop
            return real_unwrap(func, stop=lambda obj: _is_mocked(obj) or _stop(func))
        except Exception as e:
            warnings.warn(
                f"Got {e!r} when unwrapping {func!r}.  This is usually caused "
                "by a violation of Python's object protocol; see e.g. "
                "https://github.com/pytest-dev/pytest/issues/5080",
                PytestWarning,
            )
            raise

    inspect.unwrap = _mock_aware_unwrap
    try:
        yield
    finally:
        inspect.unwrap = real_unwrap

