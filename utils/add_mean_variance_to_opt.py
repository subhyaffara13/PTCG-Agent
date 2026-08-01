
def add_mean_variance_to_opt(
    opt: base.GradientTransformation,
    ema_decay: jax.typing.ArrayLike = 0.9,
    per_elt_axis: int | list[int] = 0,
    accumulation_steps: int = 1,
):
  r"""Add mean and variance to an optimizer.

  Args:
    opt: The optimizer to add mean and variance to.
    ema_decay: The EMA decay factor.
    per_elt_axis: The axis to average over.
    accumulation_steps: The number of microbatches to accumulate over.

  Returns:
    An optax GradientTransformation that adds mean and variance to an optimizer.

  Example:
  >>> import jax
  >>> import jax.numpy as jnp
  >>> import jax.random as jrd
  >>> import optax
  >>> from optax.experimental import aggregating
  >>> num_microbatches = 3
  >>> size_microbatch = 4
  >>> output_dim = 2
  >>> input_dim = 2
  >>> xs = jrd.normal(
  ...     jrd.key(0), (num_microbatches, size_microbatch, input_dim)
  ... )
  >>> ys = jrd.normal(
  ...     jrd.key(1), (num_microbatches, size_microbatch, output_dim)
  ... )
  >>> params = jrd.normal(jrd.key(2), (input_dim, output_dim))
  >>> opt = optax.adam(learning_rate=0.01)
  >>> opt = aggregating.add_mean_variance_to_opt(
  ...     opt=opt,
  ...     ema_decay=0.9,
  ...     per_elt_axis=0,
  ...     num_microbatches=1,
  ... )
  >>> fun = lambda w, x, y: jnp.mean(jnp.sum((x.dot(w)-y)**2, axis=-1))
  >>> values_and_grads = jax.vmap(jax.value_and_grad(fun), (None, 0, 0))
  >>> state = opt.init(params)
  >>> for i, (x, y) in enumerate(zip(xs, ys)):
  ...   full_loss = fun(params, xs, ys)
  ...   losses, grads = values_and_grads(params, x, y)
  ...   updates, state = opt.update(grads, state)
  ...   params = optax.apply_updates(params, updates)
  ...   mean_ema, var_ema = aggregating.get_unbiased_mean_and_variance_ema(
  ...       state
  ...   )
  ...   print(f'Step: {i}|Batch loss: {jnp.mean(losses):.2e}')
  ...   print(f'Mean EMA:\n {mean_ema}\nVariance EMA:\n {var_ema}')
  Step: 0|Batch loss: 7.46e+00
  Mean EMA:
  [[ 2.8991693e-04  3.8409345e+00]
  [-1.1956869e+00  4.7318892e+00]]
  Variance EMA:
  [[ 4.3785257 48.656933 ]
  [ 3.8709724 77.66371  ]]
  Step: 1|Batch loss: 5.52e+00
  Mean EMA:
  [[ 1.2733988  3.0736945]
  [-3.0100226  3.1490781]]
  Variance EMA:
  [[29.188576 30.26823 ]
  [13.972735 49.39477 ]]
  Step: 2|Batch loss: 5.15e+00
  Mean EMA:
  [[ 1.244118   2.2072985]
  [-2.719866   3.0309222]]
  Variance EMA:
  [[23.888937  27.574411 ]
  [12.0260725 32.332287 ]]
  """
  return process(
      preprocessor=base.identity(),
      aggregator=get_per_element_mean_and_sum_sq_diff_grads(
          per_elt_axis, accumulation_steps
      ),
      postprocessor=_combining.chain(
          track_per_element_mean_and_variance_with_ema(ema_decay),
          opt,
      ),
      aggregator_has_aux=True,
  )

