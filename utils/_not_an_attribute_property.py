
def _not_an_attribute_property(name: str):
  def _op(self):
    raise AttributeError(
      f"'{type(self).__name__}' object has no attribute '{name}'"
    )

  return property(_op)

