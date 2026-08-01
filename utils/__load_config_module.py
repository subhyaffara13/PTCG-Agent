
def _LoadConfigModule(name: str, path: str):
  """Loads a script from external file specified by path.

  Unprefixed path is looked for in the current working directory using
  regular file open operation. This should work with relative config paths.

  Args:
    name: Name of the new module.
    path: Path to the .py file containing the module.

  Returns:
    Module loaded from the given path.

  Raises:
    IOError: If the config file cannot be found.
  """
  if not path:
    raise IOError('Path to config file is an empty string.')

  ignoring_errors = _IgnoreFileNotFoundAndCollectErrors()

  # Works for relative paths.
  with ignoring_errors.Attempt('Relative path', path):
    config_module = _load_source(name, path)
    return config_module

  # Nothing worked. Log the paths that were attempted.
  raise IOError('Failed loading config file {}\n{}'.format(
      name, ignoring_errors.DescribeAttempts()))

