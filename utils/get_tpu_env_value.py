import os

def get_tpu_env_value(key) -> str | None:
  # First try to get the value from the environment.
  value = os.environ.get(key, None)
  if value is None:
    # If not found, try to get it from the metadata.
    value = get_tpu_env_value_from_metadata(key)
  return value

