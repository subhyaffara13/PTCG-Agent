
def preprocess_step(
    timestep: rl_environment.TimeStep, num_players
) -> rl_environment.TimeStep:
  # TODO(author5): fix for our time steps (should be multiple discounts)
  if timestep.discounts is None:
    timestep = timestep._replace(discounts=[1.0] * num_players)
  if timestep.rewards is None:
    timestep = timestep._replace(rewards=[0.0] * num_players)
  # print(timestep)
  return tree.map_structure(_preprocess_none, timestep)

