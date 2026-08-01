
def get_per_element_mean_and_sum_sq_diff_grads(
    per_elt_axis: int | Sequence[int] = 0,
    accumulation_steps: int = 1,
) -> Aggregator:
  """Collect per-element mean and sum square diff gradients.

  See :func:`optax.experimental.aggregating.add_mean_variance_to_opt` for an
  example on how to use this function.

  Args:
    per_elt_axis: The axis to average over.
    accumulation_steps: The number of microbatches to accumulate over.

  Returns:
    An Aggregator that collects per-element mean and sum square diff gradients.
  """

  def compute_avg_and_sum_sq_diff(
      per_elt_udpates: base.Updates,
      state: base.OptState,
      params: base.Params | None,
  ) -> tuple[base.Updates, base.Updates]:
    del params
    batch_size = get_batch_size_from_per_elt_updates(
        per_elt_udpates, per_elt_axis
    )
    mean_grads = jax.tree.map(
        lambda x: jnp.mean(x, axis=per_elt_axis, keepdims=True),
        per_elt_udpates,
    )
    sum_sq_diff_grads = jax.tree.map(
        lambda x, a: jnp.sum((x - a)**2, axis=per_elt_axis),
        per_elt_udpates,
        mean_grads,
    )
    mean_grads = jax.tree.map(
        lambda x: x.squeeze(axis=per_elt_axis), mean_grads
    )
    aux_data = {
        'sum_sq_diff_grads': sum_sq_diff_grads,
        'sample_size': batch_size,
    }
    return (mean_grads, aux_data), state

  if accumulation_steps == 1:
    return Aggregator(base.init_empty_state, compute_avg_and_sum_sq_diff)

  def init_fn(params):
    return PerElementMeanAndSumSqDiffGradsState(
        micro_step=jnp.asarray(0, dtype=jnp.int32),
        ready=jnp.asarray(False),
        mean_grads=tree.zeros_like(params),
        sum_sq_diff_grads=tree.zeros_like(params),
    )

  def update_fn(per_elt_udpates, state, params=None):
    del params
    batch_size = get_batch_size_from_per_elt_updates(
        per_elt_udpates, per_elt_axis
    )
    new_micro_step = state.micro_step + 1

    # Compute batch averages.
    batch_mean_grads = jax.tree.map(
        lambda x: jnp.mean(x, axis=per_elt_axis, keepdims=True), per_elt_udpates
    )
    batch_sum_sq_diff_grads = jax.tree.map(
        lambda x, a: jnp.sum(jnp.square(x - a), axis=per_elt_axis),
        per_elt_udpates,
        batch_mean_grads,
    )
    batch_mean_grads = jax.tree.map(
        lambda x: x.squeeze(axis=per_elt_axis), batch_mean_grads
    )

    # Update accumulated averages.
    delta = jax.tree.map(lambda u, a: u - a, batch_mean_grads, state.mean_grads)
    new_mean_grads = jax.tree.map(
        lambda a, d: a + d / new_micro_step,
        state.mean_grads,
        delta,
    )
    size_factor = state.micro_step * batch_size / new_micro_step
    new_sum_sq_diff_grads = jax.tree.map(
        lambda a, s, d: a + s + d**2 * size_factor,
        state.sum_sq_diff_grads,
        batch_sum_sq_diff_grads,
        delta,
    )
    maybe_outputs = (
        new_mean_grads,
        {
            'sum_sq_diff_grads': new_sum_sq_diff_grads,
            'sample_size': batch_size * new_micro_step,
        },
    )

    # Output or not the accumulated averages.
    ready_state = PerElementMeanAndSumSqDiffGradsState(
        micro_step=jnp.asarray(0, dtype=jnp.int32),
        ready=jnp.asarray(True),
        mean_grads=tree.zeros_like(new_mean_grads),
        sum_sq_diff_grads=tree.zeros_like(new_sum_sq_diff_grads),
    )
    not_ready_state = PerElementMeanAndSumSqDiffGradsState(
        micro_step=new_micro_step,
        ready=jnp.asarray(False),
        mean_grads=new_mean_grads,
        sum_sq_diff_grads=new_sum_sq_diff_grads,
    )
    updates, new_state = tree.where(
        new_micro_step == accumulation_steps,
        (maybe_outputs, ready_state),
        (tree.zeros_like(maybe_outputs), not_ready_state),
    )
    return updates, new_state

  return Aggregator(init_fn, update_fn)

