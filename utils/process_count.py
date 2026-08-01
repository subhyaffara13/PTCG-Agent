
def process_count() -> int:
  return jax.process_count()


def process_count() -> int:
  return jax.process_count()


def process_count(
    backend: str | xla_client.Client | None = None
) -> int:
  """Returns the number of JAX processes associated with the backend."""
  gen = (d.process_index for d in devices(backend))
  return max(gen, default=0) + 1

