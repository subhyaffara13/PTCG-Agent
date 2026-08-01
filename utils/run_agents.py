
def run_agents(
    agents: typing.List[OpponentShapingAgent],
    env: rl_environment.Environment,
    num_steps=1000,
):
  time_step = env.reset()
  for _ in range(num_steps):
    actions = []
    for agent in agents:
      action, _ = agent.step(time_step)
      if action is not None:
        action = action.squeeze()
      actions.append(action)
    if time_step.last():
      time_step = env.reset()
    else:
      time_step = env.step(actions)
      time_step.observations['actions'] = np.array(actions)

