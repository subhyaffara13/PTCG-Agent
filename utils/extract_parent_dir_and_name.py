
def extract_parent_dir_and_name(
    infos: Sequence[types.ParamInfo],
) -> tuple[Sequence[str], Sequence[str]]:
  """Extracts names and locations from ParamInfos."""
  parent_dirs = [str(info.parent_dir) for info in infos]
  names = [str(info.name) for info in infos]
  return parent_dirs, names

