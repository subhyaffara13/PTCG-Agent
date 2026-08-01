
def _forward_operator_to_aval(name):
  def op(self, *args):
    return getattr(self.aval, f"_{name}")(self, *args)
  return op

