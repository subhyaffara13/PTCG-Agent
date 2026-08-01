
def _mlp_forwards(mlp_hidden_sizes: List[int]) -> hk.Transformed:
  """Returns a haiku transformation of the MLP model to be used in optimizer.

  Args:
    mlp_hidden_sizes: List containing size of linear layers.

  Returns:
    Haiku transformation of the RNN network.
  """
  def forward_fn(inputs):
    mlp = hk.nets.MLP(mlp_hidden_sizes, activation=jax.nn.relu, name="mlp")
    return mlp(inputs)
  return hk.transform(forward_fn)


def _mlp_forwards(mlp_hidden_sizes: List[int]) -> hk.Transformed:
  """Returns a haiku transformation of the MLP model to be used in optimizer.

  Args:
    mlp_hidden_sizes: List containing size of linear layers.

  Returns:
    Haiku transformation of the RNN network.
  """
  def forward_fn(inputs):
    mlp = hk.nets.MLP(mlp_hidden_sizes, activation=jax.nn.relu, name="mlp")
    return mlp(inputs)
  return hk.transform(forward_fn)

