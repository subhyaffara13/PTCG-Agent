
def _check(cond, message=None):  # noqa: F811
    r"""Throws error containing an optional message if the specified condition
    is False.

    Error type: ``RuntimeError``

    C++ equivalent: ``TORCH_CHECK``

    Args:
        cond (:class:`bool`): If False, throw error

        message (Callable, optional): Callable that returns either a string or
            an object that has a ``__str__()`` method to be used as the error
            message. Default: ``None``
    """
    _check_with(RuntimeError, cond, message)  # pyrefly: ignore [bad-argument-type]


def _check(x, msg):
    if not x:
        raise SchemaUpdateError(msg)


def _check(roots):
    # this is the desired invariant for roots returned
    # by all_roots. It is trivially true for linear
    # polynomials.
    nreal = sum(1 if i.is_real else 0 for i in roots)
    assert sorted(roots[:nreal]) == list(roots[:nreal])
    for ix in range(nreal, len(roots), 2):
        if not (
                roots[ix + 1] == roots[ix] or
                roots[ix + 1] == conjugate(roots[ix])):
            return False
    return True


def _check(pred, msg, debug, *fmt_args, **fmt_kwargs):
  if not is_scalar_pred(pred):
    prim_name = 'debug_check' if debug else 'check'
    raise TypeError(f'{prim_name} takes a scalar pred as argument, got {pred}')
  for arg in jtu.tree_leaves((fmt_args, fmt_kwargs)):
    if not isinstance(arg, (Array, np.ndarray)):
      raise TypeError('Formatting arguments to checkify.check need to be '
                      'PyTrees of arrays, but got '
                      f'{arg!r} of type {type(arg)}.')
  new_error = FailedCheckError(get_traceback(), msg, *fmt_args, **fmt_kwargs)
  error = assert_func(init_error, jnp.logical_not(pred), new_error)
  _check_error(error, debug=debug)


def _check(partitions, unreduced, reduced):
  if not reduced and not unreduced:
    return
  if None in unreduced:
    raise ValueError(
        "unreduced cannot contain None. All elements in unreduced should refer"
        " to the mesh axes.")
  if None in reduced:
    raise ValueError(
        "reduced cannot contain None. All elements in reduced should refer"
        " to the mesh axes.")
  if unreduced & reduced:
    raise ValueError(
        "`unreduced` and `reduced` argument to PartitionSpec cannot overlap. "
        f"Got unreduced: {unreduced} and reduced: {reduced}")

  for partition in partitions:
    partition = partition if isinstance(partition, tuple) else (partition,)
    for p in partition:
      if p in unreduced:
        raise ValueError(
            "partitions cannot overlap with unreduced axes passed to"
            f" PartitionSpec. Got partitions: {partitions} and unreduced axes:"
            f" {unreduced}")
      if p in reduced:
        raise ValueError(
            "partitions cannot overlap with reduced axes passed to"
            f" PartitionSpec. Got partitions: {partitions} and reduced axes:"
            f" {reduced}")

