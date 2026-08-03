from typing import Callable

def _argnums_partial(_fun: Callable,
                     _dyn_argnums: Sequence[int],
                     _fixed_args: Sequence, *dyn_args, **kwargs):
  sentinel = object()
  args = [sentinel] * (len(_fixed_args) + len(dyn_args))
  for i, arg in zip(_dyn_argnums, dyn_args):
    args[i] = arg
  fixed_args_ = iter(_fixed_args)
  args = [next(fixed_args_).val if x is sentinel else x for x in args]
  assert next(fixed_args_, sentinel) is sentinel
  return _fun(*args, **kwargs)

