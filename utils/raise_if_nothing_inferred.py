import sys
from typing import Callable

def raise_if_nothing_inferred(
    func: Callable[_P, Generator[InferenceResult]],
) -> Callable[_P, Generator[InferenceResult]]:
    def inner(*args: _P.args, **kwargs: _P.kwargs) -> Generator[InferenceResult]:
        generator = func(*args, **kwargs)
        try:
            yield next(generator)
        except StopIteration as error:
            # generator is empty
            if error.args:
                raise InferenceError(**error.args[0]) from error
            raise InferenceError(
                "StopIteration raised without any error information."
            ) from error
        except RecursionError as error:
            raise InferenceError(
                f"RecursionError raised with limit {sys.getrecursionlimit()}."
            ) from error

        yield from generator

    return inner

