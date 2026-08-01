
def _train_avg_policy(agent):
  """Trains the average policy network."""
  num_epoch = 8
  epoch_steps = int(np.ceil(agent.cfg.avg_policy_batch_steps / num_epoch))

  buf = agent.avg_policy_buffer
  dataset = torch.utils.data.TensorDataset(
      torch.from_numpy(buf.experience.state),
      torch.from_numpy(buf.experience.policy),
      torch.from_numpy(buf.experience.t),
  )
  optimizer = torch.optim.Adam(
      agent.avg_policy_net.parameters(), lr=agent.cfg.avg_policy_learning_rate
  )

  for _ in range(num_epoch):
    agent.avg_policy_t += 1

    agent.avg_policy_net.train()
    for _ in range(epoch_steps):
      indices = np.random.choice(
          len(buf), size=(agent.cfg.avg_policy_batch_size,), replace=False
      )
      batch = Behaviour(
          state=dataset.tensors[0][indices],
          policy=dataset.tensors[1][indices],
          t=dataset.tensors[2][indices],
      )

      loss = _get_avg_policy_loss(agent, batch)
      optimizer.zero_grad()
      loss.backward()
      optimizer.step()

