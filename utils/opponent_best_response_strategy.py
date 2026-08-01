
def opponent_best_response_strategy(utility):
  opponent_action = jnp.argmin(utility, axis=-1)
  opponent_strategy = jax.nn.one_hot(opponent_action, FLAGS.num_actions)
  return opponent_strategy

