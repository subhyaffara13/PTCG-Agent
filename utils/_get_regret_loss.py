
def _get_regret_loss(agent, player, batch):
  """Returns the loss for the regret network."""
  x = batch.state.to(torch.float32)
  mask = batch.mask
  y_regret = batch.regret

  regret = agent.regret_nets[player](x)

  loss = torch.pow(regret - y_regret, 2)

  # Linear CFR.
  weight = batch.t / agent.t
  weight = weight.unsqueeze(-1).expand(-1, loss.shape[-1])
  loss = torch.mul(loss, weight)

  loss = torch.sum(torch.mul(loss, mask)) / torch.sum(mask)
  return loss

