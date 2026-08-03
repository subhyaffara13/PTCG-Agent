from typing import List

def collect_batch(
    env: Environment, agents: List[OpponentShapingAgent], eval_mode: bool
) -> List[TimeStep]:
  """Collects one episode.

  Args:
      env: The environment.
      agents: A list of opponent shaping agents.
      eval_mode: If true, the agents will be run in evaluation mode.

  Returns:
      A list of time steps.
  """
  episode = []
  time_step = env.reset()
  episode.append(time_step)
  while not time_step.last():
    actions = []
    for agent in agents:
      action, _ = agent.step(time_step, is_evaluation=eval_mode)
      if action is not None:
        action = action.squeeze()
      actions.append(action)
    time_step = env.step(np.stack(actions, axis=1))
    time_step.observations['actions'] = actions
    episode.append(time_step)

  for agent in agents:
    agent.step(time_step, is_evaluation=eval_mode)
  return episode

