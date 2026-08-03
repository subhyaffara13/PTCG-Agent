import logging

def create_constant_learning_rate_schedule(
  base_learning_rate, steps_per_epoch, warmup_length=0.0
):
  """Create a constant learning rate schedule with optional warmup.

  Note that with `FLIP #1009`_ learning rate schedules in ``flax.training`` are
  **effectively deprecated** in favor of Optax_ schedules. Please refer to
  `Optimizer Schedules`_ for more information.

  .. _FLIP #1009: https://github.com/google/flax/blob/main/docs/flip/1009-optimizer-api.md
  .. _Optax: https://github.com/deepmind/optax
  .. _Optimizer Schedules: https://optax.readthedocs.io/en/latest/api.html#optimizer-schedules

  Holds the learning rate constant. This function also offers a learing rate
  warmup as per https://arxiv.org/abs/1706.02677, for the purpose of training
  with large mini-batches.

  Args:
    base_learning_rate: the base learning rate
    steps_per_epoch: the number of iterations per epoch
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

  def learning_rate_fn(step):
    lr = base_learning_rate
    if warmup_length > 0.0:
      lr = lr * jnp.minimum(1.0, step / float(warmup_length) / steps_per_epoch)
    return lr

  return learning_rate_fn

