
def check_pytree(pytree):
  """Checks if a pytree is valid."""
  if not isinstance(pytree, Pytree):
    raise TypeError(f'Expected a Pytree, got {type(pytree)}.')

  for name, value in vars(pytree).items():
    pytree._check_value(name, value, new_status=None)

