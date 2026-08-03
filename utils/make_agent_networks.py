from typing import Tuple

def make_agent_networks(
    num_actions: int,
) -> Tuple[hk.Transformed, hk.Transformed]:
  def policy(obs):
    logits = hk.nets.MLP(output_sizes=[8, 8, num_actions], with_bias=True)(obs)
    logits = jnp.nan_to_num(logits)
    return distrax.Categorical(logits=logits)

  def value_fn(obs):
    values = hk.nets.MLP(output_sizes=[8, 8, 1], with_bias=True)(obs)
    return values

  return hk.without_apply_rng(hk.transform(policy)), hk.without_apply_rng(
      hk.transform(value_fn)
  )


def make_agent_networks(
    num_states: int, num_actions: int
) -> Tuple[hk.Transformed, hk.Transformed]:
  """Creates action weights for each state-action pair and values for each state.

  Args:
      num_states: The number of distinct states.
      num_actions: The number of distinct actions.

  Returns:
      A tuple of policy and critic networks transformed by hk.transform.
  """

  def policy(obs):
    theta = hk.get_parameter(
        'theta',
        init=hk.initializers.Constant(0),
        shape=(num_states, num_actions),
    )
    logits = jnp.select(obs, theta)
    logits = jnp.nan_to_num(logits)
    return distrax.Categorical(logits=logits)

  def value_fn(obs):
    w = hk.get_parameter(
        'w', [num_states], init=jnp.zeros
    )  # @pylint: disable=invalid-name
    return w[jnp.argmax(obs, axis=-1)].reshape(*obs.shape[:-1], 1)

  return hk.without_apply_rng(hk.transform(policy)), hk.without_apply_rng(
      hk.transform(value_fn)
  )

