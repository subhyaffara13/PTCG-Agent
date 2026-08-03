import sys

def mark_adhoc_imported_modules(
    source: None | g3_utils.Source,
) -> Iterator[None]:
  """Mark modules that were adhoc imported from this context.

  This allow `reload_workspace=True` to raise an error if the source change.

  Args:
    source: The source of the adhoc import

  Yields:
    None
  """
  old_modules = set(sys.modules)
  try:
    yield
  finally:
    adhoc_imported_modules = set(sys.modules) - old_modules
    for module_name in adhoc_imported_modules:
      # TODO(epot): Could check that the `source` and `.__file__` match
      sys.modules[module_name]._etils_workspace_reload_source = source  # pylint: disable=protected-access

