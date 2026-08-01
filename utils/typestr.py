
def typestr(*objs: object) -> str:
    if len(objs) == 1:
        (obj,) = objs
        if isinstance(obj, VariableTracker):
            return str(obj)
        else:
            return type(obj).__name__
    else:
        return " ".join(map(typestr, objs))


def typestr(handler_cls: Type[CheckpointableHandler]) -> str:
  """A name for the handler class that uniquely identifies it."""
  return f'{handler_cls.__module__}.{handler_cls.__qualname__}'


def typestr(handler_cls: Type[LeafHandler]) -> str:
  """A name for the handler class that uniquely identifies it."""
  return f'{handler_cls.__module__}.{handler_cls.__qualname__}'

