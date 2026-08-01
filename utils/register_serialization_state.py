
def register_serialization_state(
  ty, ty_to_state_dict, ty_from_state_dict, override=False
):
  """Register a type for serialization.

  Args:
    ty: the type to be registered
    ty_to_state_dict: a function that takes an instance of ty and
      returns its state as a dictionary.
    ty_from_state_dict: a function that takes an instance of ty and
      a state dict, and returns a copy of the instance with the restored state.
    override: override a previously registered serialization handler
      (default: False).
  """
  if ty in _STATE_DICT_REGISTRY and not override:
    raise ValueError(
      f'a serialization handler for "{ty.__name__}" is already registered'
    )
  _STATE_DICT_REGISTRY[ty] = (ty_to_state_dict, ty_from_state_dict)

