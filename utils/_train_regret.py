
def _train_regret(cfg, agent):
  """Trains the regret network."""
  for player in range(cfg.game.num_players()):
    _train_value(cfg, agent, player)
    _gather_regret_data(cfg.game, agent, player)

    num_epoch = 8
    epoch_steps = int(np.ceil(agent.cfg.regret_batch_steps / num_epoch))
    buf = agent.regret_buffers[player]
    dataset = torch.utils.data.TensorDataset(
        torch.from_numpy(buf.experience.state),
        torch.from_numpy(buf.experience.regret),
        torch.from_numpy(buf.experience.mask),
        torch.from_numpy(buf.experience.t),
    )
    regret_net = agent.regret_nets[player]
    regret_net.reset()
    optimizer = torch.optim.Adam(
        regret_net.parameters(), lr=agent.cfg.regret_learning_rate
    )

    for _ in range(num_epoch):
      agent.regret_t += 1

      for _ in range(epoch_steps):
        indices = np.random.choice(
            len(buf), size=(agent.cfg.regret_batch_size,), replace=False
        )
        batch = StateRegret(
            state=dataset.tensors[0][indices],
            regret=dataset.tensors[1][indices],
            mask=dataset.tensors[2][indices],
            t=dataset.tensors[3][indices],
        )

        loss = _get_regret_loss(agent, player, batch)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

