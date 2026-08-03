from typing import Any

def _process_inputs(args, kwargs) -> Any:
  """A function that normalizes the representation of the ``args`` and
  ``kwargs`` for the ``inputs`` column.
  """
  if args and kwargs:
    input_values = (*args, kwargs)
  elif args and not kwargs:
    input_values = args[0] if len(args) == 1 else args
  elif kwargs and not args:
    input_values = kwargs
  else:
    input_values = ()

  return input_values

