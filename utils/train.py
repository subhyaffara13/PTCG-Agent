import logging
from typing import Callable

def train(cfg, agent):
  """Trains an Escher agent.

  Args:
      cfg: (TrainConfig) The configuration for the training.
      agent: (Agent) The Escher agent to be trained.
  """
  device = torch.device(cfg.device)
  agent.avg_policy_net.to(device)
  for i in range(len(agent.regret_nets)):
    agent.regret_nets[i].to(device)
    agent.value_nets[i].to(device)

  for _ in range(cfg.iterations):
    _train_regret(cfg, agent)

    if agent.t % cfg.evaluation_interval == 0:
      _train_avg_policy(agent)
      if cfg.nashconv:
        conv = _calc_nashconv(cfg.game, agent)
        logging.info(
            "iteration %d states %d nashconv %f",
            agent.t,
            agent.num_touched,
            conv,
        )
      reward = _play_against_random(cfg.game, agent, cfg.games_vs_random)
      logging.info(
          "iteration %d states %d reward_vs_random %f",
          agent.t,
          agent.num_touched,
          reward,
      )

    agent.t += 1


def train(
    model: DeepNeurdModel,
    data: torch.utils.data.Dataset,
    batch_size: int,
    step_size: float = 1.0,
    threshold: float = 2.0,
    autoencoder_loss: Callable = None,  # pylint: disable=g-bare-generic
) -> None:
  """Train NeuRD `model` on `data`."""
  data = torch.utils.data.DataLoader(data, batch_size=batch_size, shuffle=True)
  optimiser = torch.optim.SGD(model.parameters(), lr=step_size)

  for x, regrets in data:
    optimiser.zero_grad()

    outputs = model(x, autoencode=autoencoder_loss is not None)
    logits = outputs[:, 0]
    logits = logits - torch.mean(logits)

    regrets = thresholded(logits, regrets, threshold=threshold).detach()
    utility = F.cross_entropy(logits, regrets)

    if autoencoder_loss is not None:
      utility = utility + autoencoder_loss(x, outputs[:, 1:])

    utility.backward()
    optimiser.step()

