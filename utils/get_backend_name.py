
def get_backend_name(backend: db_schema.StorageBackend) -> str:
  """Returns a user-friendly name for the backend type.

  Args:
    backend: The StorageBackend target.

  Returns:
    A string representation of the backend type (e.g., "GCS", "Lustre",
    "unknown").
  """
  if backend.backend_type == db_schema.BackendType.BACKEND_TYPE_GCS:
    return "GCS"
  elif backend.backend_type == db_schema.BackendType.BACKEND_TYPE_LUSTRE:
    return "Lustre"
  else:
    return "unknown"

