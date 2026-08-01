
def get_storage_path(
    backend: db_schema.StorageBackend,
    relative_path: str,
) -> str:
  """Builds the absolute storage path for the given backend and relative path.

  Combines the backend's prefix with the relative path, ensuring proper
  formatting.

  Args:
    backend: The StorageBackend target.
    relative_path: The relative path of the asset.

  Returns:
    The absolute storage path.
  """
  return f"{backend.prefix.rstrip('/')}/{relative_path.lstrip('/')}"

