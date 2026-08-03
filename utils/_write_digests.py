import json

def _write_digests(path: epath.PathLike, digests: dict[str, str]) -> None:
  """Writes per-host digests to a JSON file, creating parent dirs."""
  p = epath.Path(path)
  p.parent.mkdir(parents=True, exist_ok=True)
  p.write_text(json.dumps(digests, indent=2))

