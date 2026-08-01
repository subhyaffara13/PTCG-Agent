
def _make_abstract_method(name, func):
  @wraps(func)
  def method(*args, **kwargs):
    raise NotImplementedError(f"Cannot call abstract method {name}")
  return abc.abstractmethod(method)

