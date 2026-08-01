
def random_state(state: np.random.Generator) -> np.random.Generator: ...


def random_state(
    state: int | np.ndarray | np.random.BitGenerator | np.random.RandomState | None,
) -> np.random.RandomState: ...


def random_state(state: RandomState | None = None):
    """
    Helper function for processing random_state arguments.

    Parameters
    ----------
    state : int, array-like, BitGenerator, Generator, np.random.RandomState, None.
        If receives an int, array-like, or BitGenerator, passes to
        np.random.RandomState() as seed.
        If receives an np.random RandomState or Generator, just returns that unchanged.
        If receives `None`, returns np.random.
        If receives anything else, raises an informative ValueError.

        Default None.

    Returns
    -------
    np.random.RandomState or np.random.Generator. If state is None, returns np.random

    """
    if is_integer(state) or isinstance(state, (np.ndarray, np.random.BitGenerator)):
        return np.random.RandomState(state)
    elif isinstance(state, np.random.RandomState):
        return state
    elif isinstance(state, np.random.Generator):
        return state
    elif state is None:
        return np.random
    else:
        raise ValueError(
            "random_state must be an integer, array-like, a BitGenerator, Generator, "
            "a numpy RandomState, or None"
        )

