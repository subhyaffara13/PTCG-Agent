
def _train_value(cfg, agent, player):
  """Trains the value network."""
  _gather_value_data(cfg.game, agent, player)

  num_epoch = 8
  epoch_steps = int(np.ceil(agent.cfg.value_batch_steps / num_epoch))
  buf = agent.value_buffers[player]
  dataset = torch.utils.data.TensorDataset(
      torch.from_numpy(buf.experience.state),
      torch.from_numpy(buf.experience.action),
      torch.from_numpy(buf.experience.value),
  )
  value_net = agent.value_nets[player]
  value_net.reset()
  optimizer = torch.optim.Adam(
      value_net.parameters(), lr=agent.cfg.value_learning_rate
  )

  for _ in range(num_epoch):
    agent.value_t += 1

    agent.value_nets[player].train()
    for _ in range(epoch_steps):
      indices = np.random.choice(
          len(buf), size=(agent.cfg.value_batch_size,), replace=False
      )
      batch = StateActionValue(
          state=dataset.tensors[0][indices],
          action=dataset.tensors[1][indices],
          value=dataset.tensors[2][indices],
      )

      loss = _get_value_loss(agent, player, batch)

      optimizer.zero_grad()
      loss.backward()
      optimizer.step()

