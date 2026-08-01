
def _train(
    opt,
    accumulation_steps: int = 1,
    num_samples: int = 16,
    batch_size: int = 4,
    dim: int = 4,
    num_classes: int = 2,
    metrics_ema_decay: float = 0.0,
):
  """Synthetic training with the given optimizer."""
  microbatch_size = batch_size // accumulation_steps

  def data_iterator(key):
    inputs_key, targets_key = jrd.split(key)
    inputs = jrd.normal(inputs_key, (num_samples, dim))
    targets = jrd.normal(targets_key, (num_samples, num_classes))

    for i in range(0, num_samples, microbatch_size):
      yield inputs[i : i + microbatch_size], targets[i : i + microbatch_size]

  def loss_fun(params, batch):
    inputs, targets = batch
    return jnp.mean(jnp.sum((inputs.dot(params) - targets) ** 2, -1))

  data_key, param_key = jrd.split(jrd.key(0))
  full_data = [
      jnp.concatenate(a, axis=0) for a in zip(*data_iterator(data_key))
  ]
  params = jrd.normal(param_key, (dim, num_classes))

  @jax.jit
  def train_step(params, state, batch):
    mean_grads = None
    var_grads = None
    if isinstance(opt, aggregating.Aggregator):
      losses, grads = jax.vmap(jax.value_and_grad(loss_fun), (None, 0))(
          params, batch
      )
      loss = jnp.mean(losses)
      if accumulation_steps == 1:
        mean_grads = jax.tree.map(lambda g: jnp.mean(g, axis=0), grads)
        var_grads = jax.tree.map(lambda g: jnp.var(g, axis=0, ddof=1), grads)
    else:
      loss, grads = jax.value_and_grad(loss_fun)(params, batch)
    updates, state = opt.update(grads, state)
    params = update.apply_updates(params, updates)
    return params, state, loss, mean_grads, var_grads

  state = opt.init(params)
  metrics = {}
  true_mean_grads_ema = jnp.zeros_like(params)
  true_var_grads_ema = jnp.zeros_like(params)
  for i, batch in enumerate(data_iterator(data_key)):
    full_batch_loss = loss_fun(params, full_data)
    params, state, loss, true_mean_grads, true_var_grads = train_step(
        params, state, batch
    )
    step_metrics = {'loss': loss, 'full_batch_loss': full_batch_loss}
    if isinstance(opt, aggregating.Aggregator) and (accumulation_steps == 1):
      true_mean_grads_ema, true_var_grads_ema = jax.tree.map(
          lambda x, y: (1.0 - metrics_ema_decay) * x + metrics_ema_decay * y,
          (true_mean_grads, true_var_grads),
          (true_mean_grads_ema, true_var_grads_ema),
      )
      unbiased_true_mean_grads_ema = true_mean_grads_ema / (
          1 - metrics_ema_decay ** (i + 1)
      )
      unbiased_true_var_grads_ema = true_var_grads_ema / (
          1 - metrics_ema_decay ** (i + 1)
      )
      step_metrics['true_mean_grads_ema'] = unbiased_true_mean_grads_ema
      step_metrics['true_var_grads_ema'] = unbiased_true_var_grads_ema
    try:
      mean_grads_ema, var_grads_ema = (
          aggregating.get_unbiased_mean_and_variance_ema(state)
      )
      step_metrics['mean_grads_ema'] = mean_grads_ema
      step_metrics['var_grads_ema'] = var_grads_ema
    except ValueError:
      pass
    if not metrics:
      for key in step_metrics:
        metrics[key] = []
    for key, value in step_metrics.items():
      metrics[key].append(value)
  return params, metrics

