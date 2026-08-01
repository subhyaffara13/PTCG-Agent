
def _actions(state_vec):
  """Returns the player actions that have been taken in the game so far."""
  # See UncontestedBiddingState::InformationStateTensor
  # The first 52 elements are the cards held, then two elements for each
  # possible action, specifying which of the two players has taken it (if
  # either player has). Then two elements specifying which player we are.
  actions = state_vec[52:-2]
  return [index // 2 for index, value in enumerate(actions) if value]

