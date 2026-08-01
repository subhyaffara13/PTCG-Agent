
def compile_time_strobelight_meta(
    phase_name: str,
) -> Callable[[Callable[_P, _T]], Callable[_P, _T]]:
    def compile_time_strobelight_meta_inner(
        function: Callable[_P, _T],
    ) -> Callable[_P, _T]:
        @functools.wraps(function)
        def wrapper_function(*args: _P.args, **kwargs: _P.kwargs) -> _T:
            if "skip" in kwargs and isinstance(
                skip := kwargs["skip"],
                int,
            ):
                kwargs["skip"] = skip + 1

            # This is not needed but we have it here to avoid having profile_compile_time
            # in stack traces when profiling is not enabled.
            if not StrobelightCompileTimeProfiler.enabled:
                return function(*args, **kwargs)

            return StrobelightCompileTimeProfiler.profile_compile_time(
                function, phase_name, *args, **kwargs
            )

        return wrapper_function

    return compile_time_strobelight_meta_inner

