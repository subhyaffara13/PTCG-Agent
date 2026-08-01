
def host_id(backend: str | xla_client.Client | None = None) -> int:
  warnings.warn(
      "jax.process_index has been renamed to jax.process_index. This alias "
      "will eventually be removed; please update your code.")
  return process_index(backend)

