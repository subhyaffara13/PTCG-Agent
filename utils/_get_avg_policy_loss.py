
def _get_avg_policy_loss(agent, batch):
  """Returns the loss for the average policy network."""
  x = batch.state.to(torch.float32)
  y_policy = batch.policy

  logits = agent.avg_policy_net(x)

  loss = torch.nn.functional.cross_entropy(logits, y_policy)

  # Linear CFR.
  weight = batch.t / agent.t
  loss = torch.mul(loss, weight)

  return torch.mean(loss)

