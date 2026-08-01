
def periodic_update(
    new_tensors: base.Params,
    old_tensors: base.Params,
    steps: jax.typing.ArrayLike,  # int
    update_period: jax.typing.ArrayLike,  # int
) -> base.Params:
  """Periodically update all parameters with new values.

  A slow copy of a model's parameters, updated every K actual updates, can be
  used to implement forms of self-supervision (in supervised learning), or to
  stabilize temporal difference learning updates (in reinforcement learning).

  Args:
    new_tensors: the latest value of the tensors.
    old_tensors: a slow copy of the model's parameters.
    steps: number of update steps on the "online" network.
    update_period: every how many steps to update the "target" network.

  Returns:
    a slow copy of the model's parameters, updated every `update_period` steps.

  References:
    [Grill et al., 2020](https://arxiv.org/abs/2006.07733)
    [Mnih et al., 2015](https://arxiv.org/abs/1312.5602)
  """
  return jax.lax.cond(
      jnp.mod(steps, update_period) == 0,
      lambda _: new_tensors,
      lambda _: old_tensors,
      None,
  )

