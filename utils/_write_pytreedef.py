import json
from typing import Any

def _write_pytreedef(directory: Any, pytree_repr: dict[str, Any],
                     distinct_locations: bool):
  """Write the pytreedef to the destination directory and aux data to the archive."""
  if not (jax.process_index() == 0 or distinct_locations):
    return
  root = _norm_path(directory)
  (root / _PYTREEDEF_FILE).write_text(json.dumps(pytree_repr, indent=2))

