
def iterate(func, x):
    """ Repeatedly apply a function func onto an original input

    Yields x, then func(x), then func(func(x)), then func(func(func(x))), etc..

    >>> def inc(x):  return x + 1
    >>> counter = iterate(inc, 0)
    >>> next(counter)
    0
    >>> next(counter)
    1
    >>> next(counter)
    2

    >>> double = lambda x: x * 2
    >>> powers_of_two = iterate(double, 1)
    >>> next(powers_of_two)
    1
    >>> next(powers_of_two)
    2
    >>> next(powers_of_two)
    4
    >>> next(powers_of_two)
    8
    """
    while True:
        yield x
        x = func(x)


def iterate(data):
    wrapper = get_df_wrapper()
    return wrapper.iterate(data)


def iterate(func, start):
    """Return ``start``, ``func(start)``, ``func(func(start))``, ...

    Produces an infinite iterator. To add a stopping condition,
    use :func:`take`, ``takewhile``, or :func:`takewhile_inclusive`:.

    >>> take(10, iterate(lambda x: 2*x, 1))
    [1, 2, 4, 8, 16, 32, 64, 128, 256, 512]

    >>> collatz = lambda x: 3*x + 1 if x%2==1 else x // 2
    >>> list(takewhile_inclusive(lambda x: x!=1, iterate(collatz, 10)))
    [10, 5, 16, 8, 4, 2, 1]

    """
    with suppress(StopIteration):
        while True:
            yield start
            start = func(start)


def iterate(results_: _Sequence[_ods_ir.Type], iter_space: _ods_ir.Value, init_args: _Sequence[_ods_ir.Value], crd_used_lvls: _Union[_Any, _ods_ir.IntegerAttr], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _Union[_ods_ir.OpResult, _ods_ir.OpResultList, IterateOp]:
  op = IterateOp(results_=results_, iterSpace=iter_space, initArgs=init_args, crdUsedLvls=crd_used_lvls, loc=loc, ip=ip); results = op.results
  return results if len(results) > 1 else (results[0] if len(results) == 1 else op)


def iterate(space: Space[T_cov], items: T_cov) -> Iterator:
    """Iterate over the elements of a (batched) space.

    Args:
        space: (batched) space (e.g. `action_space` or `observation_space` from vectorized environment).
        items: Batched samples to be iterated over (e.g. sample from the space).

    Example:
        >>> from gymnasium.spaces import Box, Dict
        >>> import numpy as np
        >>> space = Dict({
        ... 'position': Box(low=0, high=1, shape=(2, 3), seed=42, dtype=np.float32),
        ... 'velocity': Box(low=0, high=1, shape=(2, 2), seed=42, dtype=np.float32)})
        >>> items = space.sample()
        >>> it = iterate(space, items)
        >>> next(it)
        {'position': array([0.77395606, 0.43887845, 0.85859793], dtype=float32), 'velocity': array([0.77395606, 0.43887845], dtype=float32)}
        >>> next(it)
        {'position': array([0.697368  , 0.09417735, 0.97562236], dtype=float32), 'velocity': array([0.85859793, 0.697368  ], dtype=float32)}
        >>> next(it)
        Traceback (most recent call last):
            ...
        StopIteration
    """
    if isinstance(space, Space):
        raise CustomSpaceError(
            f"Space of type `{type(space)}` doesn't have an registered `iterate` function. Register `{type(space)}` for `iterate` to support it."
        )
    else:
        raise TypeError(
            f"The space provided to `iterate` is not a gymnasium Space instance, type: {type(space)}, {space}"
        )


def iterate(space: Space, items) -> Iterator:
    """Iterate over the elements of a (batched) space.

    Example::

        >>> from gym.spaces import Box, Dict
        >>> space = Dict({
        ... 'position': Box(low=0, high=1, shape=(2, 3), dtype=np.float32),
        ... 'velocity': Box(low=0, high=1, shape=(2, 2), dtype=np.float32)})
        >>> items = space.sample()
        >>> it = iterate(space, items)
        >>> next(it)
        {'position': array([-0.99644893, -0.08304597, -0.7238421 ], dtype=float32),
        'velocity': array([0.35848552, 0.1533453 ], dtype=float32)}
        >>> next(it)
        {'position': array([-0.67958736, -0.49076623,  0.38661423], dtype=float32),
        'velocity': array([0.7975036 , 0.93317133], dtype=float32)}
        >>> next(it)
        StopIteration

    Args:
        space: Space to which `items` belong to.
        items: Items to be iterated over.

    Returns:
        Iterator over the elements in `items`.

    Raises:
        ValueError: Space is not an instance of :class:`gym.Space`
    """
    raise ValueError(
        f"Space of type `{type(space)}` is not a valid `gym.Space` instance."
    )

