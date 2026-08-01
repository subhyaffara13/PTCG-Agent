
def _aval_property(name):
  return property(lambda self: getattr(self.aval, name))

