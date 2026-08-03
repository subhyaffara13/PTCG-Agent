import functools

def register_ffi_target_as_batch_partitionable(name: str) -> None:
  """Registers an FFI target as batch partitionable.

  Args:
    name: the name of the target.
  """
  xla_client.register_custom_call_as_batch_partitionable(name)
  xla_bridge.register_plugin_callbacks(
      functools.partial(xla_client.register_custom_call_as_batch_partitionable,
                        name))

