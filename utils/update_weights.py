from typing import List

def update_weights(agents: List[OpponentShapingAgent]):
  """Updates the weights of the opponent models.

  Args:
      agents: A list of opponent shaping agents.

  Returns:
      None
  """
  agent: OpponentShapingAgent
  for agent in agents:
    for opp in [a for a in agents if a.player_id != agent.player_id]:
      agent.update_params(state=opp.train_state, player_id=opp.player_id)

