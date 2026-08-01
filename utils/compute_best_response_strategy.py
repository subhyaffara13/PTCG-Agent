
def compute_best_response_strategy(utility):
  actions_count = utility.shape[-1]
  opponent_action = jnp.argmin(utility, axis=-1)
  opponent_strategy = jax.nn.one_hot(opponent_action, actions_count)
  return opponent_strategy

