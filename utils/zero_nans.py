
def zero_nans() -> base.GradientTransformation:
  """A transformation which replaces NaNs with 0.

  The state of the transformation has the same tree structure as that of the
  parameters. Each leaf is a single boolean which contains True iff a NaN was
  detected in the corresponding parameter array at the last call to ``update``.
  This state is not used by the transformation internally, but lets users be
  aware when NaNs have been zeroed out.

  Returns:
    A :class:`optax.GradientTransformation`.
  """

  def init_fn(params):
    return ZeroNansState(
        found_nan=jax.tree.map(
            lambda p: jnp.array(False, dtype=jnp.bool_), params
        )
    )

  def update_fn(updates, opt_state, params=None):
    del params, opt_state
    opt_state = ZeroNansState(
        found_nan=jax.tree.map(lambda p: jnp.any(jnp.isnan(p)), updates)
    )
    updates = jax.tree.map(
        lambda p: jnp.where(jnp.isnan(p), jnp.zeros_like(p), p), updates
    )
    return updates, opt_state

  return base.GradientTransformation(init=init_fn, update=update_fn)

