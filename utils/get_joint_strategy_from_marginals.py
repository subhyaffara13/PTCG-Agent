
def get_joint_strategy_from_marginals(probabilities):
  """Returns a joint strategy tensor from a list of marginals.

  Args:
    probabilities: list of probabilities.

  Returns:
    A flat joint strategy from a list of marginals.
  """
  res = np.ones((1,), dtype=np.float64)
  for prob in probabilities:
    res = res[..., None] @ np.asarray(prob).reshape((1,) * res.ndim + (-1,))
  return res.reshape(-1)


def get_joint_strategy_from_marginals(probabilities):
  """Returns a joint strategy tensor from a list of marginals.

  Args:
    probabilities: list of list of probabilities, one for each player.

  Returns:
    A joint strategy from a list of marginals.
  """
  probas = []
  for i in range(len(probabilities)):
    probas_shapes = [1] * len(probabilities)
    probas_shapes[i] = -1
    probas.append(np.array(probabilities[i]).reshape(probas_shapes))
  return np.prod(probas)

