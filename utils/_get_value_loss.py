
def _get_value_loss(agent, player, batch):
  x = batch.state.to(torch.float32)
  y_value = batch.value

  value = agent.value_nets[player](x)
  value = torch.squeeze(value, dim=[1])

  loss = torch.pow(value - y_value, 2)
  return torch.mean(loss)

