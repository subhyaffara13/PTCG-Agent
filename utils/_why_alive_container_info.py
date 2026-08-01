
def _why_alive_container_info(container, obj_id) -> str:
  name = f'<{type(container).__name__} {id(container)}>'
  if type(container) is types.ModuleType:
    name = getattr(container, '__name__', name)
  if type(container) is types.FunctionType:
    name_ = getattr(container, '__name__', '<no-name>')
    closure = inspect.getclosurevars(container)
    keys = [k for k, v in dict(closure.nonlocals, **closure.globals).items()
            if id(v) == obj_id]
    if len(keys) == 1: return f'{name} ({name_}) closed-over variable {keys[0]}'
    elif len(keys) > 1: return (f'{name} in closed-over variables ' +
                                ', '.join(map(repr, keys)))
  if hasattr(container, '__dict__'):
    keys = [k for k in vars(container) if id(vars(container)[k]) == obj_id]
    if len(keys) == 1: return f'{name}.{keys[0]}'
    elif len(keys) > 1: return f'{name} in vars ' + ', '.join(map(repr, keys))
  if isinstance(container, (list, tuple)):
    idxs = [i for i, x in enumerate(container) if id(x) == obj_id]
    if len(idxs) == 1: return f'{name}[{idxs[0]}]'
    else: return f'{name} at indices ' + ', '.join(map(str, idxs))
  if isinstance(container, dict):
    keys = [k for k in container if id(container[k]) == obj_id]
    if len(keys) == 1: return f'{name}[{keys[0]!r}]'
    else: return f'{name} at keys ' + ', '.join(map(repr, keys))
  if isinstance(container, types.ModuleType):
    return f' named {container.__name__}'
  return name

