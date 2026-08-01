
def compute_regrets(policy_logits, action_values):
  """Compute regrets using pi and Q."""
  # Compute regret.
  policy = F.softmax(policy_logits, dim=1)
  # Avoid computing gradients for action_values.
  action_values = action_values.detach()

  baseline = compute_baseline(policy, action_values)

  regrets = torch.sum(
      F.relu(action_values - torch.unsqueeze(baseline, 1)), dim=1)

  return regrets


def compute_regrets(payoff_batch, strategy_x, strategy_y):
  values_y = -jnp.matmul(strategy_x, payoff_batch)
  values_x = jnp.transpose(
      jnp.matmul(payoff_batch, jnp.transpose(strategy_y, [0, 2, 1])), [0, 2, 1])
  value_x = jnp.matmul(
      jnp.matmul(strategy_x, payoff_batch),
      jnp.transpose(strategy_y, [0, 2, 1]))
  value_y = -value_x
  regrets_x = values_x - value_x
  regrets_y = values_y - value_y
  return regrets_x, regrets_y

