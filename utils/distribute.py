import itertools

def distribute(x):
    """ Control automatic distribution of Number over Add

    Explanation
    ===========

    This context manager controls whether or not Mul distribute Number over
    Add. Plan is to avoid distributing Number over Add in all of sympy. Once
    that is done, this contextmanager will be removed.

    Examples
    ========

    >>> from sympy.abc import x
    >>> from sympy.core.parameters import distribute
    >>> print(2*(x + 1))
    2*x + 2
    >>> with distribute(False):
    ...     print(2*(x + 1))
    2*(x + 1)
    """

    old = global_parameters.distribute

    try:
        global_parameters.distribute = x
        yield
    finally:
        global_parameters.distribute = old


def distribute(A, B):
    """ Turns an A containing Bs into a B of As

    where A, B are container types

    >>> from sympy.strategies import distribute
    >>> from sympy import Add, Mul, symbols
    >>> x, y = symbols('x,y')
    >>> dist = distribute(Mul, Add)
    >>> expr = Mul(2, x+y, evaluate=False)
    >>> expr
    2*(x + y)
    >>> dist(expr)
    2*x + 2*y
    """

    def distribute_rl(expr):
        for i, arg in enumerate(expr.args):
            if isinstance(arg, B):
                first, b, tail = expr.args[:i], expr.args[i], expr.args[i + 1:]
                return B(*[A(*(first + (arg,) + tail)) for arg in b.args])
        return expr
    return distribute_rl


def distribute(n, iterable):
    """Distribute the items from *iterable* among *n* smaller iterables.

        >>> group_1, group_2 = distribute(2, [1, 2, 3, 4, 5, 6])
        >>> list(group_1)
        [1, 3, 5]
        >>> list(group_2)
        [2, 4, 6]

    If the length of *iterable* is not evenly divisible by *n*, then the
    length of the returned iterables will not be identical:

        >>> children = distribute(3, [1, 2, 3, 4, 5, 6, 7])
        >>> [list(c) for c in children]
        [[1, 4, 7], [2, 5], [3, 6]]

    If the length of *iterable* is smaller than *n*, then the last returned
    iterables will be empty:

        >>> children = distribute(5, [1, 2, 3])
        >>> [list(c) for c in children]
        [[1], [2], [3], [], []]

    This function uses :func:`itertools.tee` and may require significant
    storage.

    If you need the order items in the smaller iterables to match the
    original iterable, see :func:`divide`.

    """
    if n < 1:
        raise ValueError('n must be at least 1')

    children = tee(iterable, n)
    return [islice(it, index, None, n) for index, it in enumerate(children)]


def distribute(num_items, num_slots, normalize=False):
  """Yields all ways of distributing `num_items` items over `num_slots` slots.

  We assume that the ordering of the slots doesn't matter.

  Args:
    num_items: The number of items to distribute.
    num_slots: The number of slots.
    normalize: Normalizes the yielded tuple to contain floats in [0, 1] summing
      to 1.

  Yields:
    A tuple T containing `num_slots` positive integers such that
    `np.sum(T) == num_items` if `normalize == False` or `np.sum(T) == 1` if
    `normalize == True'.
  """
  normalization = 1
  if normalize:
    normalization = num_items
  # This is just the standard "bars and stars" problem.
  # See https://stackoverflow.com/questions/28965734/general-bars-and-stars.
  for c in itertools.combinations(
      range(num_items + num_slots - 1), num_slots - 1):
    # The combinations give you the indices of the internal bars.
    # pylint: disable=g-complex-comprehension
    yield tuple((b - a - 1) / normalization
                for (a, b) in zip([
                    -1,
                ] + list(c),
                                  list(c) + [num_items + num_slots - 1]))

