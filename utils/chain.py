import itertools
from typing import Callable

def chain(*iterables, total=None, tqdm_class=tqdm_auto, **kwargs):
    """Equivalent of `itertools.chain`."""
    if total is None:
        try:
            total = sum(map(len, iterables))
        except (TypeError, AttributeError):
            pass
    return tqdm_class(itertools.chain(*iterables), total=total, **kwargs)


def chain(*iterables: Iterable[_T]) -> Iterator[_T]:
    for iterable in iterables:
        yield from iterable


def chain(*op_support: OperatorSupportBase) -> OperatorSupportBase:
    """Combines a sequence of `OperatorSupportBase` instances to form a single `OperatorSupportBase`
    instance by evaluating each input `OperatorSupportBase` instance, and returns False if
    any of it reports False.
    """

    def _chain(submods, node) -> bool:
        return all(x.is_node_supported(submods, node) for x in op_support)

    return create_op_support(_chain)


def chain(*rules: Callable[[_T], _T]) -> Callable[[_T], _T]:
    """
    Compose a sequence of rules so that they apply to the expr sequentially
    """
    def chain_rl(expr: _T) -> _T:
        for rule in rules:
            expr = rule(expr)
        return expr
    return chain_rl


def chain(*brules):
    """
    Compose a sequence of brules so that they apply to the expr sequentially
    """
    def chain_brl(expr):
        if not brules:
            yield expr
            return

        head, tail = brules[0], brules[1:]
        for nexpr in head(expr):
            yield from chain(*tail)(nexpr)

    return chain_brl


def chain(
    *args: base.GradientTransformation,
) -> base.GradientTransformationExtraArgs:
  """Applies a list of chainable update transformations.

  This function creates a new :func:`optax.GradientTransformation` that applies
  a sequence of gradient transformations in order. The ``init`` function of the
  new transformation constructs the optimizer state by concatenating the states
  of the individual transforms, while the ``update`` function applies the
  updates in the given order.

  Args:
    *args: an arbitrary number of ``transform``-s of
      :class:`GradientTransformation` or
      :class:`GradientTransformationExtraArgs`.

  Returns:
    A :class:`GradientTransformationExtraArgs`, created by chaining the input
    transformations. Note that independent of the argument types, the resulting
    transformation always supports extra args. Any extra arguments passed to the
    returned transformation will be passed only to those transformations in the
    chain that support extra args.

  Examples:

    A transform that scales by -0.1 the adam update:

      >>> import optax
      >>> transform1 = optax.scale_by_adam()
      >>> transform2 = optax.scale(-0.1)
      >>> chained_transform = optax.chain(transform1, transform2)
      >>> params = {'a': 1.0}
      >>> state = chained_transform.init(params)
      >>> updates = {'a': -0.5}
      >>> updates, new_state = chained_transform.update(updates, state, params)

    An optimizer in the chain might require extra args:

      >>> import optax
      >>> opt1 = optax.scale(0.1)    # scale incoming gradients
      >>> opt2 = optax.polyak_sgd()  # requires a `value` extra arg for `update`
      >>> chained_transform = optax.chain(opt1, opt2)
      >>> state = chained_transform.init(0.5)
      >>> extra_args = {"value": 1.0}
      >>> updates, new_state = chained_transform.update(
      ...     0.7, state, 0.7, **extra_args  # extra args for all transforms
      ... )
  """

  transforms = [base.with_extra_args_support(t) for t in args]
  init_fns, update_fns = zip(*transforms)

  def init_fn(params):
    return tuple(fn(params) for fn in init_fns)

  def update_fn(updates, state, params=None, **extra_args):
    if len(update_fns) != len(state):
      raise ValueError(
          'The number of updates and states has to be the same in '
          'chain! Make sure you have called init first!'
      )

    new_state = []
    for s, fn in zip(state, update_fns):
      updates, new_s = fn(updates, s, params, **extra_args)
      new_state.append(new_s)
    return updates, tuple(new_state)

  # We opt to always return the GradientTransformationExtraArgs type here,
  # instead of selecting the return type based on the arguments, since it works
  # much better with the currently available type checkers. It also means that
  # users will not get unexpected signature errors if they remove all of the
  # transformations in a chain accepting extra args.
  return base.GradientTransformationExtraArgs(init_fn, update_fn)

