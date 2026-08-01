
def compute_values_against_best_response(strategy, payoff):
  utility = jnp.matmul(strategy, payoff)
  br_strategy = compute_best_response_strategy(utility)
  return jnp.matmul(payoff, jnp.transpose(br_strategy))

