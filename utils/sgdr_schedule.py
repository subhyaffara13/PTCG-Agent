
def sgdr_schedule(
    cosine_kwargs: Iterable[dict[str, jax.typing.ArrayLike]],
) -> base.Schedule:
  """SGD with warm restarts.

  This learning rate schedule applies multiple joined cosine decay cycles.

  Args:
    cosine_kwargs: An Iterable of dicts, where each element specifies the
      arguments to pass to each cosine decay cycle. The ``decay_steps`` kwarg
      will specify how long each cycle lasts for, and therefore when to
      transition to the next cycle.

  Returns:
    schedule
      A function that maps step counts to values

  References:
    Loshchilov et al., `SGDR: Stochastic Gradient Descent with Warm Restarts
    <https://arxiv.org/abs/1608.03983>`_, 2017
  """
  boundaries = []
  schedules = []
  step = 0
  for kwargs in cosine_kwargs:
    schedules += [warmup_cosine_decay_schedule(**kwargs)]
    boundaries += [step + kwargs['decay_steps']]
    step += kwargs['decay_steps']
  return _join.join_schedules(schedules, boundaries[:-1])

