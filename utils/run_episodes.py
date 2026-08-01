
def run_episodes(envs: Sequence[rl_environment.Environment],
                 agents: Sequence[rl_agent.AbstractAgent],
                 num_episodes: int = 1,
                 is_evaluation: bool = False) -> None:
  """Runs the agents on the environments for the specified number of episodes.

  Args:
    envs: RL environments.
    agents: RL agents.
    num_episodes: Number of episodes to run.
    is_evaluation: Indicates whether the agent should use the evaluation or
      training behavior.
  """
  assert len(envs) == len(agents), 'Environments should match the agents.'
  for _ in range(num_episodes):
    for env, agent in zip(envs, agents):
      time_step = env.reset()
      while not time_step.last():
        agent_output = agent.step(time_step, is_evaluation=is_evaluation)
        if agent_output:
          action_list = [agent_output.action]
          time_step = env.step(action_list)
      # Episode is over, step all agents with final info state.
      agent.step(time_step)

