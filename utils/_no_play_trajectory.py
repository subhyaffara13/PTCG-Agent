
def _no_play_trajectory(line: str):
  """Returns the deal and bidding actions only given a text trajectory."""
  actions = [int(x) for x in line.split(' ')]
  # Usually a trajectory is NUM_CARDS chance events for the deal, plus one
  # action for every bid of the auction, plus NUM_CARDS actions for the play
  # phase. Exceptionally, if all NUM_PLAYERS players Pass, there is no play
  # phase and the trajectory is just of length NUM_CARDS + NUM_PLAYERS.
  if len(actions) == NUM_CARDS + NUM_PLAYERS:
    return tuple(actions)
  else:
    return tuple(actions[:-NUM_CARDS])

