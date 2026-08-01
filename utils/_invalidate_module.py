
def _invalidate_module(module: types.ModuleType) -> None:
  """Invalidate the module in-place."""
  module_name = module.__name__

  # https://peps.python.org/pep-0562/
  def __getattr__(name: str) -> NoReturn:  # pylint: disable=invalid-name
    """All module attribute access will raise error."""
    raise AttributeError(
        f'Cannot access {module_name}.{name} on the old module'
        f' instance.\n{module_name} was reloaded, so the new module should be'
        ' used instead.\nYou can pass `invalidate=False` to keep both old and'
        ' reloaded modules.'
    )

  module.__dict__.clear()
  module.__getattr__ = __getattr__
  # Allow `adhoc_error` to detect invalidated modules and raise better errors
  module.__etils_invalidated__ = True

