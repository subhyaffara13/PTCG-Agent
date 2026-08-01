
def empty_directory(directory: epath.PathLike) -> bool:
  directory = epath.Path(directory)
  if not directory.exists():
    return False
  for p in directory.iterdir():
    if p.is_dir():
      p.rmtree()
    else:
      p.unlink()
  return True

