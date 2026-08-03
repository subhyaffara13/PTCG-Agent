from typing import Any, Callable

def use_cpp_class(cpp_cls: type[Any]) -> Callable[[type[T]], type[T]]:
  """A decorator replacing a Python class with its C++ version at runtime."""

  def wrapper(cls):
    if cpp_cls is None:
      return cls

    exclude_methods = {'__module__', '__dict__', '__doc__'}

    for attr_name, attr in cls.__dict__.items():
      if attr_name not in exclude_methods:
        if not hasattr(_original_func(attr), "_use_cpp"):
          setattr(cpp_cls, attr_name, attr)

    cpp_cls.__doc__ = cls.__doc__
    return cpp_cls

  return wrapper

