
def calculate_advantage(gamma, norm, rewards, values, dones, device):
  """Function used to calculate the Generalized Advantage estimate."""
  with torch.no_grad():
    next_done = dones[-1]
    next_value = values[-1]
    steps = len(values)
    returns = torch.zeros_like(rewards).to(device)
    for t in reversed(range(steps)):
      if t == steps - 1:
        nextnonterminal = 1.0 - next_done
        next_return = next_value
      else:
        nextnonterminal = 1.0 - dones[t + 1]
        next_return = returns[t + 1]
      returns[t] = rewards[t] + gamma * nextnonterminal * next_return

    advantages = returns - values

  if norm:
    advantages = (advantages - advantages.mean()) / (advantages.std() + 1e-8)

  return advantages, returns

