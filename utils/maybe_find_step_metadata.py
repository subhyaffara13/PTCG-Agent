
def maybe_find_step_metadata(
    base_path: epath.PathLike,
    name_format: NameFormat[Metadata],
    *,
    step: int,
) -> Metadata | None:
  """Returns `Metadata` for `step` with `name_format` or None."""
  try:
    return name_format.find_step(base_path, step)
  except ValueError:
    return None

