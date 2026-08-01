
def glob(pattern):
  if io_mode == BackendMode.DEFAULT:
    return [
      path.rstrip('/') for path in glob_module.glob(pattern, recursive=False)
    ]
  elif io_mode == BackendMode.TF:
    return gfile.glob(pattern)
  else:
    raise ValueError('Unknown IO Backend Mode.')


def glob(pathname: AnyStr, recursive: bool = False) -> list[AnyStr]:
    """Return a list of paths matching a pathname pattern.

    The pattern may contain simple shell-style wildcards a la
    fnmatch. However, unlike fnmatch, filenames starting with a
    dot are special cases that are not matched by '*' and '?'
    patterns.

    If recursive is true, the pattern '**' will match any files and
    zero or more directories and subdirectories.
    """
    return list(iglob(pathname, recursive=recursive))

