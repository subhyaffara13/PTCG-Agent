from typing import Callable

def evaluate_callable_usecols(
    usecols: Callable[[Hashable], object],
    names: Iterable[Hashable],
) -> set[int]: ...


def evaluate_callable_usecols(
    usecols: SequenceT, names: Iterable[Hashable]
) -> SequenceT: ...


def evaluate_callable_usecols(
    usecols: Callable[[Hashable], object] | SequenceT,
    names: Iterable[Hashable],
) -> SequenceT | set[int]:
    """
    Check whether or not the 'usecols' parameter
    is a callable.  If so, enumerates the 'names'
    parameter and returns a set of indices for
    each entry in 'names' that evaluates to True.
    If not a callable, returns 'usecols'.
    """
    if callable(usecols):
        return {i for i, name in enumerate(names) if usecols(name)}
    return usecols

