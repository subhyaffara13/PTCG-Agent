
def _compose(*cmgrs):
    """
    Compose any number of dependent context managers into a single one.

    The last, innermost context manager may take arbitrary arguments, but
    each successive context manager should accept the result from the
    previous as a single parameter.

    Like :func:`jaraco.functools.compose`, behavior works from right to
    left, so the context manager should be indicated from outermost to
    innermost.

    Example, to create a context manager to change to a temporary
    directory:

    >>> temp_dir_as_cwd = _compose(pushd, temp_dir)
    >>> with temp_dir_as_cwd() as dir:
    ...     assert os.path.samefile(os.getcwd(), dir)
    """

    def compose_two(inner, outer):
        def composed(*args, **kwargs):
            with inner(*args, **kwargs) as saved, outer(saved) as res:
                yield res

        return contextlib.contextmanager(composed)

    return functools.reduce(compose_two, reversed(cmgrs))


def _compose(*funcs):
    """
    Compose 2 or more callables.
    """
    assert len(funcs) > 1, "At least 2 callables must be passed to compose"
    return reduce(_compose2, funcs)


def _compose(accumulators: AccumulatorTree) -> Accumulator:
  """Composes a PyTree of Accumulators into a single Accumulator."""

  def init(values):
    return jax.tree.map(
        lambda acc, val: acc.init(val),
        accumulators,
        values,
    )

  def update(carry, value, index):
    return jax.tree.map(
        lambda acc, car, val: acc.update(car, val, index),
        accumulators,
        carry,
        value,
    )

  def finalize(carry):
    return jax.tree.map(
        lambda acc, car: acc.finalize(car),
        accumulators,
        carry,
    )

  def aggregate(values):
    return jax.tree.map(
        lambda acc, val: acc.aggregate(val), accumulators, values
    )

  return Accumulator(init, update, finalize, aggregate)

