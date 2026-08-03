import functools

def _is_module_class(target: TransformTarget) -> bool:
  return (
    inspect.isclass(target)
    and issubclass(target, Module)
    or (isinstance(target, functools.partial))
    and _is_module_class(target.func)
  )

