import functools

def core_remat_static(
    fn,
    variables=True,
    rngs=True,
    concrete=False,
    prevent_cse=True,
    static_argnums=(),
    policy=None,
):
  """Flax functional core remat version with static_argnums."""

  static_argnums = tuple(sorted(static_argnums))

  def _repack_remat_args(dyn_args, static_args):
    """Remake arg list from static and dynamic args given static_argnums."""
    args = []
    s_cnt, d_cnt = 0, 0
    for i in range(len(dyn_args) + len(static_args)):
      if i in static_argnums:
        args.append(static_args[s_cnt])
        s_cnt += 1
      else:
        args.append(dyn_args[d_cnt])
        d_cnt += 1
    return tuple(args)

  def inner(scope_fn, repack_fn, variable_groups, rng_groups, *args):
    static_args = tuple(x for i, x in enumerate(args) if i in static_argnums)
    dyn_args = tuple(x for i, x in enumerate(args) if i not in static_argnums)

    # After JAX v0.3.16, concrete=False is a no-op and concrete=True raises
    # NotImplementedError. Starting in JAX v0.8.2, the concrete argument is
    # deprecated and will be removed in the future.
    if concrete:
      raise NotImplementedError(
          "The concrete argument is deprecated. Use static_argnums instead."
          " for more information, see"
          " https://docs.jax.dev/en/latest/jep/11830-new-remat-checkpoint.html"
      )

    @functools.partial(
        jax.remat, prevent_cse=prevent_cse, policy=policy
    )
    @functools.wraps(fn)
    def rematted(variable_groups, rng_groups, *dyn_args):
      args = _repack_remat_args(dyn_args, static_args)
      scope = scope_fn(variable_groups, rng_groups)
      y = fn(scope, *args)
      return y, repack_fn(scope)

    return rematted(variable_groups, rng_groups, *dyn_args)

  return flax.core.lift.pack(
      inner, (variables,), (variables,), (rngs,), name='remat'
  )

