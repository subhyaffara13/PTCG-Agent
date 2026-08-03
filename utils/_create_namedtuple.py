from typing import Any

def _create_namedtuple(name, fieldnames, modulename, defaults=None):
    class_ = _import_module(modulename + '.' + name, safe=True)
    if class_ is not None:
        return class_
    import collections
    t = collections.namedtuple(name, fieldnames, defaults=defaults, module=modulename)
    return t


def _create_namedtuple(
    *, module_name: str, class_name: str, attrs: Iterable[tuple[str, Any]]
) -> tuple[Any, ...]:
  """Returns a namedtuple instance with the given attributes and values, `attrs`.

  The namedtuple type is created in the current module on the fly using the
  given `module_name` and `class_name`. The two names are combined to create a
  unique class name to avoid name collisions. See `_new_namedtuple_type()` for
  more details.

  Args:
    module_name: Module name of original namedtuple saved in metadata.
    class_name: Class name of original namedtuple saved in metadata.
    attrs: The attributes of the namedtuple.
  """
  ks, vs = [*zip(*attrs)] or ((), ())
  result = _new_namedtuple_type(module_name, class_name, ks)(*vs)
  return result

