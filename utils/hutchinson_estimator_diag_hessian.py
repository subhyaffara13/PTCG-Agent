
def hutchinson_estimator_diag_hessian(random_seed: Optional[jax.Array] = None):
  """Returns a GradientTransformationExtraArgs computing the Hessian diagonal.

  The Hessian diagonal is estimated using Hutchinson's estimator, which is
  unbiased but has high variance.

  Args:
    random_seed: key used to generate random vectors.

  Returns:
    GradientTransformationExtraArgs
  """

  def init_fn(params):
    del params
    key = random_seed if random_seed is not None else jax.random.PRNGKey(0)
    return HutchinsonState(key=key)

  def update_fn(updates, state, params=None, obj_fn=None, **extra_args):
    # complies with signature of GradientTransformationExtraArgs but ignores the
    # extra_args
    del extra_args
    if params is None:
      raise ValueError("params must be provided to hutchinson update function.")
    if obj_fn is None:
      raise ValueError("obj_fn must be provided to hutchinson update function.")
    del updates
    key, subkey = jax.random.split(state.key)
    random_signs = optax.tree.random_like(
        subkey,
        params,
        jax.random.rademacher,
        dtype=jnp.float32,
    )
    random_signs = optax.tree.cast(random_signs,
                                   optax.tree.dtype(params, "lowest"))
    hvp = jax.jvp(jax.grad(obj_fn), (params,), (random_signs,))[1]
    product = jax.tree.map(lambda h, r: h * r, hvp, random_signs)
    return product, HutchinsonState(key=key)

  return base.GradientTransformationExtraArgs(init_fn, update_fn)

