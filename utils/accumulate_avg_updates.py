
def accumulate_avg_updates(
    accumulation_steps: int,
) -> base.GradientTransformation:
  """Accumulates average gradients for `accumulation_steps` microbatches.

  Best used in combination with :func:`optax.experimental.process` to define
  an optimizer accumulating gradients over multiple microbatches, see example
  below.

  Args:
    accumulation_steps: The number of microbatches to accumulate over.

  Returns:
    An optax GradientTransformation that accumulates average gradients for
    `accumulation_steps` microbatches.

  Example:
    >>> import jax
    >>> import jax.numpy as jnp
    >>> import jax.random as jrd
    >>> import optax
    >>> num_microbatches = 3
    >>> size_microbatch = 4
    >>> output_dim = 2
    >>> input_dim = 6
    >>> xs = jrd.normal(
    ...     jrd.key(0), (num_microbatches, size_microbatch, input_dim)
    ... )
    >>> ys = jrd.normal(
    ...     jrd.key(1), (num_microbatches, size_microbatch, output_dim)
    ... )
    >>> params = jrd.normal(jrd.key(2), (input_dim, output_dim))
    >>> # The following is equivalent to an effective batch size of
    >>> # accumulation_steps * size_microbatch
    >>> opt = optax.adam(learning_rate=0.01)
    >>> opt = process(
    ...     preprocessor=base.identity(),
    ...     aggregator=average_incrementally_updates(
    ...          per_elt_axis=None,
    ...          accumulation_steps=2,
    ...     ),
    ...     postprocessor=opt,
    ... )
    >>> fun = lambda w, x, y: jnp.mean(jnp.sum((x.dot(w)-y)**2, axis=-1))
    >>> state = opt.init(params)
    >>> for i, (x, y) in enumerate(zip(xs, ys)):
    ...   full_loss = fun(params, xs, ys)
    ...   loss, grads = jax.value_and_grad(fun)(params, x, y)
    ...   updates, state = opt.update(grads, state)
    ...   params = optax.apply_updates(params, updates)
    ...   print(f'Step: {i}|Batch loss: {loss:.2e}|Full loss: {full_loss:.2e}')
    Step: 0|Batch loss: 2.51e+01|Full loss: 1.49e+01
    Step: 1|Batch loss: 1.16e+01|Full loss: 1.49e+01
    Step: 2|Batch loss: 7.93e+00|Full loss: 1.46e+01
  """

  if accumulation_steps < 1:
    raise ValueError('accumulation_steps must be larger than or equal to 1.')

  if accumulation_steps == 1:
    # If there is only one microbatch, we don't need accumulation.
    # We return identity to save unnecessary state tracking.
    return base.identity()

  def init_fn(params):
    return AccumulateAvgUpdatesState(
        micro_step=jnp.asarray(0),
        ready=jnp.asarray(False),
        avg_grad=tree.zeros_like(params),
    )

  def update_fn(updates, state, params=None):
    del params
    new_micro_step = state.micro_step + 1
    new_avg_grad = jax.tree.map(
        lambda u, a: a + (u - a) / new_micro_step,
        updates,
        state.avg_grad,
    )
    ready_state = AccumulateAvgUpdatesState(
        micro_step=jnp.asarray(0),
        ready=jnp.asarray(True),
        avg_grad=tree.zeros_like(new_avg_grad),
    )
    not_ready_state = AccumulateAvgUpdatesState(
        micro_step=new_micro_step,
        ready=jnp.asarray(False),
        avg_grad=new_avg_grad,
    )
    updates, new_state = tree.where(
        new_micro_step == accumulation_steps,
        (new_avg_grad, ready_state),
        (tree.zeros_like(new_avg_grad), not_ready_state),
    )
    return updates, new_state

  return base.GradientTransformation(init_fn, update_fn)

