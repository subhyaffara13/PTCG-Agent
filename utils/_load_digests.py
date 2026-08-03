import json
import logging

def _load_digests(path: epath.PathLike) -> dict[str, str] | None:
  """Loads a per-host digests JSON file, or None if absent/unreadable."""
  try:
    p = epath.Path(path)
    if not p.exists():
      return None
    return json.loads(p.read_text()) or None
  except (OSError, ValueError) as e:
    logging.warning("Could not load digests from %s: %s", path, e)
    return None

