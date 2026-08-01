
def joint_action_probabilities(state, policy):
  """Yields action, probability pairs for a joint policy in simultaneous state.

  Args:
    state: a game state at a simultaneous decision node.
    policy: policy that gives the probability distribution over the legal
      actions for each players.

  Yields:
    (action, probability) pairs. An action is a tuple of individual
      actions for each player of the game. The probability is a single joint
      probability (product of all the individual probabilities).
  """
  actions_per_player, probs_per_player = joint_action_probabilities_aux(
      state, policy)
  for actions, probs in zip(
      itertools.product(*actions_per_player),
      itertools.product(*probs_per_player)):
    yield actions, np.prod(probs)

