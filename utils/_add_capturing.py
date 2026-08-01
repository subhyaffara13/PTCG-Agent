
def _add_capturing(cls, variable_type):
  """Adds capturing to methods of a Module.
  Does not instrument superclass methods."""
  for name, method in cls.__dict__.items():
    if callable(method) and (not name.startswith('_') or name == '__call__'):
      if not hasattr(method, '_does_capturing'):
        def closure(name, method): # Necessary to make 'name' immutable during iteration
          @ft.wraps(method)
          def wrapper(self, *args, **kwargs):
            result = method(self, *args, **kwargs)
            self.sow(variable_type, name, result)
            return result
          wrapper._does_capturing = True
          setattr(cls, name, wrapper)
        closure(name, method)
  return cls

