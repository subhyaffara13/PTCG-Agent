
def named_chain(
    *args: tuple[str, base.GradientTransformation]
) -> base.GradientTransformationExtraArgs:
  """Applies a list of named chainable update transformations.

  A variant of :func:`optax.chain` that allows to name each transformation.

  Here the ``args`` are ``(name, transformation)`` pairs, constituted of a
  string ``name`` and an associated transformation ``transformation``. The
  gradient transformation must be an instance of :class:`GradientTransformation`
  or :class:`GradientTransformationExtraArgs`.

  Each ``name`` is used as key for the state of the corresponding transformation
  within the ``named_chain`` state. Thus the state of the transformation
  with a given ``name`` can be easily retrieved as ``opt_state[name]``.

  Args:
    *args: an arbitrary number of ``(name, transform)`` pairs, constituted of a
      string ``name`` and an associated transformation ``transform``. The latter
      is a :class:`GradientTransformation` or
      :class:`GradientTransformationExtraArgs`.

  Returns:
    A single (init_fn, update_fn) tuple.

  Examples:
    >>> import optax
    >>> opt1 = optax.scale(0.1)    # scale incoming gradients
    >>> opt2 = optax.polyak_sgd()  # requires a `value` extra arg for `update`
    >>> chained_transform = optax.named_chain(("scale", opt1), ("sgd", opt2))
    >>> state = chained_transform.init(0.5)
    >>> extra_args = {"value": 1.0}
    >>> updates, new_state = chained_transform.update(
    ...     0.7, state, 0.7, **extra_args  # extra args for all transforms
    ... )
    >>> tuple(new_state.keys()) == ("scale", "sgd")
    True
  """

  names = [name for name, _ in args]

  if len(names) != len(set(names)):
    raise ValueError(
        f'Named transformations must have unique names, but got {names}'
    )

  transforms = [
      (name, base.with_extra_args_support(t)) for name, t in args
  ]

  def init_fn(params):
    # Explicitly use an ordered dict, to preserve the order of the
    # transformations. This is useful for inspecting the state because pytree
    # traversal canonicalizes (sorts) the keys in regular dicts.
    states = collections.OrderedDict()
    for name, tx in transforms:
      states[name] = tx.init(params)
    return states

  def update_fn(updates, state, params=None, **extra_args):
    new_state = collections.OrderedDict()
    for name, tx in transforms:
      updates, new_state[name] = tx.update(
          updates, state[name], params, **extra_args
      )
    return updates, new_state

  return base.GradientTransformationExtraArgs(init_fn, update_fn)

