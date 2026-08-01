
def set_tnp() -> None:
  """Enable numpy behavior (for `tensorflow`).

  Note: The fixture has to be explicitly declared in the `_test.py`
  file where it is used. This can be done by assigning
  `set_tnp = enp.testing.set_tnp`.
  """
  # This is required to have TF follow the same casting rules as numpy
  lazy.tnp.experimental_enable_numpy_behavior(prefer_float32=True)

