from typing import Any

def _namedtuple_state_dict(nt) -> dict[str, Any]:
  return {key: to_state_dict(getattr(nt, key)) for key in nt._fields}

