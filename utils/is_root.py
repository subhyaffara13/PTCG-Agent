
def is_root(key, player):
  empty_is_key = f"***EMPTY_INFOSET_P{player}***"
  empty_isa_key = f"***EMPTY_INFOSET_ACTION_P{player}***"
  return True if key in [empty_is_key, empty_isa_key] else False

