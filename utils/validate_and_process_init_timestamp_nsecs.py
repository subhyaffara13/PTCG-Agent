from typing import Any

def validate_and_process_init_timestamp_nsecs(
    init_timestamp_nsecs: Any,
) -> int | None:
  """Validates and processes init_timestamp_nsecs field."""
  if init_timestamp_nsecs is None:
    return None

  _validate_type(init_timestamp_nsecs, int)
  return init_timestamp_nsecs

