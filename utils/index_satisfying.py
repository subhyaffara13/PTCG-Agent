
def index_satisfying(iterable, condition):
    """Returns the index of the first element in `iterable` that
    satisfies the given condition.

    If no such element is found (that is, when the iterable is
    exhausted), this returns the length of the iterable (that is, one
    greater than the last index of the iterable).

    `iterable` must not be empty. If `iterable` is empty, this
    function raises :exc:`ValueError`.

    """
    # Pre-condition: iterable must not be empty.
    for i, x in enumerate(iterable):
        if condition(x):
            return i
    # If we reach the end of the iterable without finding an element
    # that satisfies the condition, return the length of the iterable,
    # which is one greater than the index of its last element. If the
    # iterable was empty, `i` will not be defined, so we raise an
    # exception.
    try:
        return i + 1
    except NameError as err:
        raise ValueError("iterable must be non-empty") from err

