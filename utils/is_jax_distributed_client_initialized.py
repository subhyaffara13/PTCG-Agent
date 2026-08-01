
def is_jax_distributed_client_initialized() -> bool:
  """Returns True if the JAX distributed client is initialized."""
  return jax._src.distributed.global_state.client is not None  # pylint: disable=protected-access

