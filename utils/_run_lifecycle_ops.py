import logging
from typing import Callable

def _run_lifecycle_ops(*ops: Callable[[], None]) -> None:
  """Runs all lifecycle operations and re-raises the first failure."""
  first_error = None
  for op in ops:
    try:
      op()
    except Exception as e:  # pylint: disable=broad-exception-caught
      if first_error is None:
        first_error = e
      else:
        logging.exception(
            'Additional colocated checkpoint lifecycle operation failed.'
        )
  if first_error is not None:
    raise first_error

