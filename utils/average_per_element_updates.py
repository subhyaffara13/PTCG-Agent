
def average_per_element_updates(
    per_elt_axis: int | Sequence[int] = 0,
) -> Aggregator:
  """Average per-element updates.

  Args:
    per_elt_axis: The axis to average over.

  Returns:
    An Aggregator that averages per-element updates.
  """

  def update_fn(per_elt_updates, state, params=None):
    del params
    avg_updates = jax.tree.map(
        lambda x: jnp.mean(x, axis=per_elt_axis), per_elt_updates
    )
    return avg_updates, state

  return Aggregator(base.init_empty_state, update_fn)

