
def _forward_property_to_aval(name):
  def prop(self):
    return getattr(self.aval, name).fget(self)
  return property(prop)

