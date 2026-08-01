
def process_indices(
    backend: str | xla_client.Client | None = None
) -> list[int]:
  """Returns the list of all JAX process indices associated with the backend.

  Args:
    backend: This is an experimental feature and the API is likely to change.
      Optional, a string representing the xla backend: ``'cpu'``, ``'gpu'``, or
      ``'tpu'``.

  Returns:
    List of integer process indices.
  """
  return list(range(process_count(backend)))

