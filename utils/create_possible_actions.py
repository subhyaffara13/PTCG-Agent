
def create_possible_actions():
  actions = []
  for player in range(_NUM_PLAYERS):
    for tile in _DECK:
      for edge in _EDGES:
        if edge in tile or edge is None:  # can we play tile on edge?
          actions.append(Action(player, tile, edge))
  return actions


def create_possible_actions():
  actions = []
  for player in range(_NUM_PLAYERS):
    for tile in _DECK:
      for edge in _EDGES:
        if edge in tile or edge is None:
          actions.append(Action(player, tile, edge))
  return actions

