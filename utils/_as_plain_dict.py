
def _as_plain_dict(obj: Any) -> dict[str, Any] | None:
  """Returns a dataclass or dict as a plain dict, else None."""
  if dataclasses.is_dataclass(obj):
    return dataclasses.asdict(obj)
  return obj if isinstance(obj, dict) else None

