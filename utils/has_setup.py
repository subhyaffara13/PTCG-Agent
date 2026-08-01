
def has_setup(x: tp.Any) -> tp.TypeGuard[_HasSetup]:
  return hasattr(x, 'setup')

