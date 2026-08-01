
def is_async_checkpointer(checkpointer: AbstractCheckpointer):
  return isinstance(
      checkpointer, async_checkpointer.AsyncCheckpointer
  ) or isinstance(
      checkpointer,
      jax_serialization.GlobalAsyncCheckpointManagerBase,
  )

