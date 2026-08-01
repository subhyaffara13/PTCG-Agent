
def create_cosine_learning_rate_schedule(
  base_learning_rate, steps_per_epoch, halfcos_epochs, warmup_length=0.0
):
  """Create a cosine learning rate schedule with optional warmup.

  Note that with `FLIP #1009`_ learning rate schedules in ``flax.training`` are
  **effectively deprecated** in favor of Optax_ schedules. Please refer to
  `Optimizer Schedules`_ for more information.

  .. _FLIP #1009: https://github.com/google/flax/blob/main/docs/flip/1009-optimizer-api.md
  .. _Optax: https://github.com/deepmind/optax
  .. _Optimizer Schedules: https://optax.readthedocs.io/en/latest/api.html#optimizer-schedules

  A cosine learning rate schedule modules the learning rate with
  half a cosine wave, gradually scaling it to 0 at the end of training.

  This function also offers a learing rate warmup as per
  https://arxiv.org/abs/1706.02677, for the purpose of training with large
  mini-batches.

  Args:
    base_learning_rate: the base learning rate
    steps_per_epoch: the number of iterations per epoch
    halfcos_epochs: the number of epochs to complete half a cosine wave;
      normally the number of epochs used for training
    warmup_length: if > 0, the learning rate will be modulated by a warmup
      factor that will linearly ramp-up from 0 to 1 over the first
      ``warmup_length`` epochs

  Returns:
    Function ``f(step) -> lr`` that computes the learning rate for a given step.
  """
  logging.warning(
    'Learning rate schedules in ``flax.training`` are effectively deprecated '
    'in favor of Optax schedules. Please refer to '
    'https://optax.readthedocs.io/en/latest/api.html#optimizer-schedules'
    ' for alternatives.'
  )
  halfwavelength_steps = halfcos_epochs * steps_per_epoch

  def learning_rate_fn(step):
    scale_factor = jnp.cos(step * jnp.pi / halfwavelength_steps) * 0.5 + 0.5
    lr = base_learning_rate * scale_factor
    if warmup_length > 0.0:
      lr = lr * jnp.minimum(1.0, step / float(warmup_length) / steps_per_epoch)
    return lr

  return learning_rate_fn

