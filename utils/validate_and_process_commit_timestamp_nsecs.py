
def validate_and_process_commit_timestamp_nsecs(
    commit_timestamp_nsecs: Any,
) -> int | None:
  """Validates and processes commit_timestamp_nsecs field."""
  if commit_timestamp_nsecs is None:
    return None

  _validate_type(commit_timestamp_nsecs, int)
  return commit_timestamp_nsecs

