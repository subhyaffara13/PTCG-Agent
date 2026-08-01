
def join_effects(*effects: Effects) -> Effects:
  return set().union(*effects) if effects else no_effects

