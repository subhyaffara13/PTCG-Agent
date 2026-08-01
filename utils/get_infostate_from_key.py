
def get_infostate_from_key(isa_key, player):
  assert not is_root(isa_key, player), "Cannot use this method for root nodes."
  infostate, _ = isa_key.split(_DELIMITER)
  return infostate

