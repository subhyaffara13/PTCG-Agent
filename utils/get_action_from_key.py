
def get_action_from_key(isa_key):
  _, action_str = isa_key.split(_DELIMITER)
  return int(action_str)

