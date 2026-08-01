
def build_step_path(
    base_path: epath.PathLike, name_format: NameFormat[Metadata], step: int
) -> epath.Path:
  """Returns `step` path under `base_path` for step `name_format`."""
  return epath.Path(base_path) / name_format.build_name(step)

