
def _update_old_module(
    old_module: types.ModuleType,
    new_module: types.ModuleType,
) -> None:
  """Mutate the old module version with the new dict.

  This also try to update the class, functions,... from the old module (so
  instances are updated in-place).

  Args:
    old_module: Old module to update
    new_module: New module
  """
  # Replace the old dict by the new module content
  old_module.__dict__.clear()
  old_module.__dict__.update(new_module.__dict__)

