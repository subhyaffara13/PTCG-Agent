from typing import Any

def to_state_dict(target) -> dict[str, Any]:
  """Returns a dictionary with the state of the given target."""
  if _is_namedtuple(target):
    ty = _NamedTuple
  else:
    ty = type(target)
  if ty not in _STATE_DICT_REGISTRY:
    return target

  ty_to_state_dict = _STATE_DICT_REGISTRY[ty][0]
  state_dict = ty_to_state_dict(target)
  if isinstance(state_dict, dict):
    for key in state_dict.keys():
      assert isinstance(key, str), 'A state dict must only have string keys.'
  return state_dict

