
def host_ids(
    backend: str | xla_client.Client | None = None
) -> list[int]:
  warnings.warn(
      "jax.process_indexs has been renamed to jax.process_indices. This alias "
      "will eventually be removed; please update your code.")
  return process_indices(backend)

