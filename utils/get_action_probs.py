import itertools
from typing import List

def get_action_probs(
    agent: OpponentShapingAgent, game: str
) -> List[typing.Dict[str, typing.Any]]:
  """Returns the probability of cooperation and a string repr for each state.
  
  Args:
      agent: The agent.
      game: The name of the game.

  Returns:
      A list of dictionaries, each containing the probability of cooperation
      and a string representation
  """
  actions = ['C', 'D'] if game == 'ipd' else ['H', 'T']
  states = ['s0'] + [''.join(s) for s in itertools.product(actions, repeat=2)]
  params = agent.train_state.policy_params[agent.player_id]
  action_probs = []
  for i, state_str in enumerate(states):
    state = np.eye(len(states))[i]
    prob = agent.policy_network.apply(params, state).prob(0)
    action = actions[0]
    action_probs.append(
        {'prob': prob.item(), 'name': f'P({action}|{state_str})'}
    )
  return action_probs

