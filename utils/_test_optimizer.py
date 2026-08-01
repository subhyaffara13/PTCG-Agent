
def _test_optimizer(step_size: float) -> base.GradientTransformation:
  """Inner optimizer for the Mechanic tests."""

  # Use SGD for simplicity but add non-trivial optimizer state so that the
  # resetting behavior of lookahead can be tested.
  def init_fn(params):
    aggregate_grads = jax.tree.map(jnp.zeros_like, params)
    return OptimizerTestState(aggregate_grads)

  def update_fn(updates, state, params):
    # The test optimizer does not use the parameters, but we check that they
    # have been passed correctly.
    test_utils.assert_trees_all_equal_shapes(updates, params)
    aggregate_grads = update.apply_updates(state.aggregate_grads, updates)
    updates = jax.tree.map(lambda u: step_size * u, updates)
    return updates, OptimizerTestState(aggregate_grads)

  return base.GradientTransformation(init_fn, update_fn)


def _test_optimizer(step_size: float) -> base.GradientTransformation:
  """Fast optimizer for the lookahead tests."""

  # Use SGD for simplicity but add non-trivial optimizer state so that the
  # resetting behavior of lookahead can be tested.
  def init_fn(params):
    aggregate_grads = jax.tree.map(jnp.zeros_like, params)
    return OptimizerTestState(aggregate_grads, is_reset=True)

  def update_fn(updates, state, params):
    # The test optimizer does not use the parameters, but we check that they
    # have been passed correctly.
    test_utils.assert_trees_all_equal_shapes(updates, params)
    aggregate_grads = update.apply_updates(state.aggregate_grads, updates)
    updates = jax.tree.map(lambda u: step_size * u, updates)
    return updates, OptimizerTestState(aggregate_grads, is_reset=False)

  return base.GradientTransformation(init_fn, update_fn)

