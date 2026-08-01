
def _has_zarray_files(path: epath.Path) -> List[bool]:
  return [(p / '.zarray').exists() for p in path.iterdir() if p.is_dir()]

