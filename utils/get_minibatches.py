
def get_minibatches(
    batch: TransitionBatch, num_minibatches: int
) -> typing.Iterator[TransitionBatch]:
  """Yields an iterator over minibatches of the given batch.

  Args:
      batch: A transition batch.
      num_minibatches: The number of minibatches to return.

  Yields:
      An iterator over minibatches of the given batch.
  """

  def get_minibatch(x, start, end):
    return x[:, start:end] if len(x.shape) > 2 else x

  for i in range(num_minibatches):
    start, end = i * (batch.reward.shape[1] // num_minibatches), (i + 1) * (
        batch.reward.shape[1] // num_minibatches
    )
    mini_batch = jax.tree_util.tree_map(
        partial(get_minibatch, start=start, end=end), batch
    )
    yield mini_batch

