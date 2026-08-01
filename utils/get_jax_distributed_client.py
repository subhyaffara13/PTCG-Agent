
def get_jax_distributed_client():
  client = jax._src.distributed.global_state.client  # pylint: disable=protected-access
  if client is None:
    raise ValueError(
        'Distributed system is not available; please initialize it via '
        '`jax.distributed.initialize()` at the start of your program.'
    )
  return client

