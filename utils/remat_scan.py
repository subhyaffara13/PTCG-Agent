
def remat_scan(
  body_fn: Callable[..., Any],
  lengths: Sequence[int],
  policy: Callable[..., bool] | None = None,
  variable_broadcast: CollectionFilter = False,
  variable_carry: CollectionFilter = False,
  variable_axes: Mapping[CollectionFilter, InOutScanAxis] = {True: 0},
  split_rngs: Mapping[PRNGSequenceFilter, bool] = {True: True},
) -> Callable[..., Any]:
  """Combines `lift.remat` and `lift.scan` for memory efficiency and constant time compilation.

  ``remat_scan`` allows for constant compile times and sublinear
  memory usage with respect to model depth. At a small constant
  penalty. This is typically beneficial for very deep models.

  Example::

    def body_fn(scope, x):
      return nn.dense(scope, x, features=x.shape[-1])
    # 100x dense with O(sqrt(N)) memory for gradient computation
    y = lift.remat_scan(body_fn, lengths=(10, 10))(scope, x)

  Args:
    body_fn: Scope function to be repeated using a (nested scan)
    lengths: number of loop iterations at the given level. The total number of
      iterations `n = prod(lengths)`. each loop is rematerialized. This way the
      memory consumption is proportional to `n^(1 / d)` where `d =
      len(lengths)`. Minimal memory consumptions requires tuning the lengths
      such that the same amount of memory is consumed at each level of the
      nested loop.
    policy: Experimental checkpoint policy, see ``jax.checkpoint``.
    variable_broadcast: Specifies the broadcasted variable collections. A
      broadcasted variable should not depend on any computation that cannot be
      lifted out of the loop. This is typically used to define shared parameters
      inside the fn.
    variable_carry: Specifies the variable collections that are carried through
      the loop. Mutations to these variables are carried to the next iteration
      and will be preserved when the scan finishes.
    variable_axes: the variable collections that are scanned over.
    split_rngs: Split PRNG sequences will be different for each loop iterations.
      If split is False the PRNGs will be the same across iterations.
  Returns:
    A wrapped version of ``body_fn`` that repeats itself prod(lengths) times.
  """
  # TODO(jheek) should remat scan have scan inputs/outputs?
  scan_fn = functools.partial(
    scan,
    variable_broadcast=variable_broadcast,
    variable_carry=variable_carry,
    variable_axes=variable_axes,
    split_rngs=split_rngs,
  )
  if len(lengths) == 1:

    def wrapper(scope, carry):
      return body_fn(scope, carry), ()

    fn = lambda scope, c: scan_fn(wrapper, length=lengths[0])(scope, c)[0]
  else:

    @functools.partial(remat, policy=policy, prevent_cse=False)
    def inner_loop(scope, carry):
      carry = remat_scan(
        body_fn,
        lengths[1:],
        policy,
        variable_broadcast,
        variable_carry,
        variable_axes,
        split_rngs,
      )(scope, carry)
      return carry, ()

    fn = lambda scope, c: scan_fn(inner_loop, length=lengths[0])(scope, c)[0]
  return fn


def remat_scan(
  target: Target,
  lengths: Sequence[int] | None = (),
  policy: Callable[..., bool] | None = None,
  variable_broadcast: CollectionFilter = False,
  variable_carry: CollectionFilter = False,
  variable_axes: Mapping[CollectionFilter, InOutScanAxis] = FrozenDict(
    {True: 0}
  ),
  split_rngs: Mapping[PRNGSequenceFilter, bool] = FrozenDict({True: True}),
) -> Target:
  """Combines remat and scan for memory efficiency and constant time compilation.

  ``remat_scan`` allows for constant compile times and sublinear
  memory usage with respect to model depth. At a small constant
  penalty. This is typically beneficial for very deep models.

  Example::

    >>> import flax.linen as nn

    >>> class BigModel(nn.Module):
    ...   @nn.compact
    ...   def __call__(self, x):
    ...     DenseStack = nn.remat_scan(nn.Dense, lengths=(10, 10))
    ...     # 100x dense with O(sqrt(N)) memory for gradient computation
    ...     return DenseStack(8, name="dense_stack")(x)

  Args:
    target: a ``Module`` or a function taking a ``Module`` as its first
      argument.
    lengths: number of loop iterations at the given level. The total number of
      iterations ``n = prod(lengths)``. each loop is rematerialized. This way the
      memory consumption is proportional to ``n^(1 / d)`` where ``d =
      len(lengths)``. Minimal memory consumptions requires tuning the lengths
      such that the same amount of memory is consumed at each level of the
      nested loop.
    policy: Experimental checkpoint policy, see ``jax.checkpoint``.
    variable_broadcast: Specifies the broadcasted variable collections. A
      broadcasted variable should not depend on any computation that cannot be
      lifted out of the loop. This is typically used to define shared parameters
      inside the fn.
    variable_carry: Specifies the variable collections that are carried through
      the loop. Mutations to these variables are carried to the next iteration
      and will be preserved when the scan finishes.
    variable_axes: the variable collections that are scanned over. Defaults to
      ``{True: 0}``.
    split_rngs: Split PRNG sequences will be different for each loop iterations.
      If split is False the PRNGs will be the same across iterations. Defaults
      to ``{True: True}``.

  Returns:
    A wrapped version of ``target`` that repeats itself prod(lengths) times.
  """
  return lift_transform(
    lift.remat_scan,
    target,
    lengths=lengths,
    variable_broadcast=variable_broadcast,
    variable_carry=variable_carry,
    variable_axes=variable_axes,
    split_rngs=split_rngs,
    policy=policy,
  )

