from typing import Optional

def get_save_directory(
    step: int,
    directory: epath.PathLike,
    name: Optional[str] = None,
    step_prefix: Optional[str] = None,
    override_directory: Optional[epath.PathLike] = None,
    step_format_fixed_length: Optional[int] = None,
    step_name_format: Optional[NameFormat[Metadata]] = None,
) -> epath.Path:
  """Returns the standardized path to a save directory for a single item.

  Args:
    step: Step number.
    directory: Top level checkpoint directory.
    name: Item name ('params', 'state', 'dataset', etc.).
    step_prefix: Prefix applied to `step` (e.g. 'checkpoint').
    override_directory: If provided, step, directory, and step_prefix are
      ignored.
    step_format_fixed_length: Uses a fixed number of digits with leading zeros
      to represent the step number. If None, there are no leading zeros.
    step_name_format: NameFormat used to define step name for step and under
      given root directory. If provided, `step_prefix` and
      `step_format_fixed_length` are ignored.

  Returns:
    A directory.
  """
  if directory is None:
    raise ValueError('Directory cannot be None.')
  directory = epath.Path(directory)
  if override_directory is not None:
    result = epath.Path(override_directory)
  else:
    step_name_format = step_name_format or standard_name_format(
        step_prefix=step_prefix,
        step_format_fixed_length=step_format_fixed_length,
    )
    result = build_step_path(directory, step_name_format, step)
  if name is not None:
    result /= name
  return result

