import re
from typing import Any

def _deserialize(backend_name, obj, location):
    if backend_name == "privateuse1":
        backend_name = torch._C._get_privateuse1_backend_name()
    if location == backend_name or bool(
        re.match(f"{backend_name}(:|[0-9]+)", location)
    ):
        device = _validate_device(location, backend_name)
        return obj.to(device=device)


def _deserialize(serialized: bytes) -> Any:
  """Deserializes callables and input/output spec objects.

  DO NOT USE THIS FUNCTION EXCEPT FOR THE INTERNAL IMPLEMENTATION OF
  colocated_python. See serialize() for details.

  Raises:
    ModuleNotFoundError: If cloudpickle is not available.
  """
  if cloudpickle is None:
    raise ModuleNotFoundError('No module named "cloudpickle"')

  assert _common_obj_state.common_obj is None, (
      "_deserialize() expects no recursive calls")
  _common_obj_state.common_obj = []
  try:
    return cloudpickle.loads(serialized)
  finally:
    _common_obj_state.common_obj = None

