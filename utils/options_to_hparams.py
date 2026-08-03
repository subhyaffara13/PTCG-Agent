from typing import Any

def options_to_hparams(options: Any) -> dict[str, bool | int | float | str]:
  """Flattens an options dataclass/dict into a TB HParams-acceptable form.

  HParams values must be primitives; anything else (None, list, tuple, nested)
  is `str()`-ified so the run still appears in Parallel Coordinates instead of
  being dropped.

  Args:
    options: An options dataclass instance or dict.

  Returns:
    A flat dict of primitive HParams values; empty if options is neither a
    dataclass nor a dict.
  """
  if dataclasses.is_dataclass(options):
    raw = dataclasses.asdict(options)
  elif isinstance(options, dict):
    raw = dict(options)
  else:
    return {}
  out: dict[str, bool | int | float | str] = {}
  for k, v in raw.items():
    if isinstance(v, (bool, int, float, str)):
      out[k] = v
    else:
      out[k] = str(v)
  return out

