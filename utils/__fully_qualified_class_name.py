
def _FullyQualifiedClassName(klass):
  module = klass.__module__
  name = getattr(klass, '__qualname__', klass.__name__)
  if module in (None, 'builtins', '__builtin__'):
    return name
  return module + '.' + name

