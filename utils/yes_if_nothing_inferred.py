
def yes_if_nothing_inferred(
    func: Callable[_P, Generator[InferenceResult]],
) -> Callable[_P, Generator[InferenceResult]]:
    def inner(*args: _P.args, **kwargs: _P.kwargs) -> Generator[InferenceResult]:
        generator = func(*args, **kwargs)

        try:
            yield next(generator)
        except StopIteration:
            # generator is empty
            yield util.Uninferable
            return

        yield from generator

    return inner

