
def split_real_and_imaginary(
    inner: base.GradientTransformation,
) -> base.GradientTransformation:
  """Splits the real and imaginary components of complex updates into two.

  The inner transformation processes real parameters and updates, and the
  pairs of transformed real updates are merged into complex updates.

  Parameters and updates that are real before splitting are passed through
  unmodified.

  Args:
    inner: The inner transformation.

  Returns:
    An `optax.GradientTransformation`.
  """

  def init_fn(params):
    params = jax.tree.map(_complex_to_real_pair, params)
    inner_state = inner.init(params)
    return SplitRealAndImaginaryState(inner_state)

  def update_fn(updates, state, params=None):
    inner_state = state.inner_state
    updates = jax.tree.map(_complex_to_real_pair, updates)
    params = jax.tree.map(_complex_to_real_pair, params)
    updates, inner_state = inner.update(updates, inner_state, params)
    updates = jax.tree.map(
        _real_pair_to_complex,
        updates,
        is_leaf=lambda x: isinstance(x, SplitRealAndImaginaryArrays),
    )
    return updates, SplitRealAndImaginaryState(inner_state)

  return base.GradientTransformation(init_fn, update_fn)

