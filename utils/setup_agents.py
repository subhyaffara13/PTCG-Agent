
def setup_agents(
    env: Environment, rng: hk.PRNGSequence
) -> List[OpponentShapingAgent]:
  """Creates an opponent shaping agent for each player in the environment.

  Args:
      env: The environment.
      rng: A random seed key.

  Returns:
      A list of opponent shaping agents.
  """
  agents = []
  num_actions = env.action_spec()['num_actions']
  info_state_shape = env.observation_spec()['info_state']
  for player_id in range(env.num_players):
    networks = make_agent_networks(
        num_states=info_state_shape[player_id][0],
        num_actions=num_actions[player_id],
    )
    agent = make_agent(
        key=next(rng), player_id=player_id, env=env, networks=networks
    )
    agents.append(agent)
  return agents

