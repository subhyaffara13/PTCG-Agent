import logging

def print_directory(directory: epath.PathLike, level: int = 0):
  """Prints a directory tree for debugging purposes."""
  directory = epath.Path(directory)
  if not directory.exists():
    raise ValueError(f'Directory {directory} does not exist.')
  if not directory.is_dir():
    raise ValueError(f'Directory {directory} is not a directory.')
  level_str = '..' * level
  if level == 0:
    logging.info('Printing directory tree: %s/', directory)
  else:
    logging.info('%s%s/', level_str, directory.name)

  level_str = '..' * (level + 1)
  for p in directory.iterdir():
    if p.is_dir():
      print_directory(p, level=level + 1)
    else:
      logging.info('%s%s', level_str, p.name)

