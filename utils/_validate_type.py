from typing import Any

def _validate_type(obj: Any, field_type: type[Any] | Sequence[type[Any]]):
  if isinstance(field_type, Sequence):
    if not any(isinstance(obj, f_type) for f_type in field_type):
      raise ValueError(
          f'Object must be any one of types {list(field_type)}, got '
          f'{type(obj)}.'
      )
  elif not isinstance(obj, field_type):
    raise ValueError(f'Object must be of type {field_type}, got {type(obj)}.')

