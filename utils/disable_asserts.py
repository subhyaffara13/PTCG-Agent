
def disable_asserts() -> None:
  """Disables all Chex assertions.

  Use wisely.
  """
  _ai.DISABLE_ASSERTIONS = True

