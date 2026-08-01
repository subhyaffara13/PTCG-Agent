
def strobelight(
    profiler: StrobelightCLIFunctionProfiler | None = None, **kwargs: Any
) -> Callable[[Callable[_P, _R]], Callable[_P, _R | None]]:
    if not profiler:
        profiler = StrobelightCLIFunctionProfiler(**kwargs)

    def strobelight_inner(
        work_function: Callable[_P, _R],
    ) -> Callable[_P, _R | None]:
        @functools.wraps(work_function)
        def wrapper_function(*args: _P.args, **kwargs: _P.kwargs) -> _R | None:
            # pyrefly: ignore [bad-argument-type]
            return profiler.profile(work_function, *args, **kwargs)

        return wrapper_function

    return strobelight_inner


def strobelight(
    profiler: StrobelightCLIFunctionProfiler | None = None, **kwargs: Any
) -> Callable[[Callable[_P, _R]], Callable[_P, _R | None]]:
    if not profiler:
        profiler = StrobelightCLIFunctionProfiler(**kwargs)

    def strobelight_inner(
        work_function: Callable[_P, _R],
    ) -> Callable[_P, _R | None]:
        @functools.wraps(work_function)
        def wrapper_function(*args: _P.args, **kwargs: _P.kwargs) -> _R | None:
            # pyrefly: ignore [bad-argument-type]
            return profiler.profile(work_function, *args, **kwargs)

        return wrapper_function

    return strobelight_inner

