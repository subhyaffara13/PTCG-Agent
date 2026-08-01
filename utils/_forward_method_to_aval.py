
def _forward_method_to_aval(name):
  def meth(self, *args, **kwargs):
    __tracebackhide__ = True
    return getattr(self.aval, name).fun(self, *args, **kwargs)
  return meth

