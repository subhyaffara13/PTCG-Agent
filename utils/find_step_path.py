
def find_step_path(
    base_path: epath.PathLike,
    name_format: NameFormat[Metadata],
    *,
    step: int,
    include_uncommitted: bool = False,
) -> epath.Path:
  """Returns `step` path under `base_path` for step `name_format`.

  NOTE: Experimental function, subject to change.

  Args:
    base_path: directory path containing step subdirs.
    name_format: NameFormat of the target `step`.
    step: target step number.
    include_uncommitted: if True then uncommitted steps are considered in search
      too, otherwise only committed steps are looked up.

  Raises:
    ValueError if the target step path does not exist.
  """
  base_path = epath.Path(base_path)
  if not include_uncommitted:
    return name_format.find_step(base_path, step).path

  # First try finding uncommitted step.
  uncommitted_step_path = None
  for tmp_path in all_temporary_paths(base_path):
    if tmp_path.get_final() == build_step_path(base_path, name_format, step):
      uncommitted_step_path = tmp_path.get()
      break
  if uncommitted_step_path and uncommitted_step_path.exists():
    return uncommitted_step_path
  # Uncommitted step not found, return committed one or raise error.
  return name_format.find_step(base_path, step).path

