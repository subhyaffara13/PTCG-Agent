from typing import List

def log_epoch_data(epoch: int, agents: List[OpponentShapingAgent], eval_batch):
  """Logs data to wandb and prints it to the console.

  Args:
      epoch: The current epoch.
      agents: A list of agents.
      eval_batch: A batch of episodes.
  """
  logs = {}
  for agent in agents:
    avg_step_reward = np.mean(
        [ts.rewards[agent.player_id] for ts in eval_batch]
    )
    probs = get_action_probs(agent, game=FLAGS.game)
    for info in probs:
      logs[f'agent_{agent.player_id}/{info["name"]}'] = info['prob']
    probs = ', '.join([f'{info["name"]}: {info["prob"]:.2f}' for info in probs])
    metrics = agent.metrics()
    logs.update({
        f'agent_{agent.player_id}/avg_step_reward': avg_step_reward,
        **{
            f'agent_{agent.player_id}/{k}': v.item() for k, v in metrics.items()
        },
    })
    print(
        f'[epoch {epoch}] Agent {agent.player_id}: {avg_step_reward:.2f} |'
        f' {probs}'
    )
  wandb.log(logs)

