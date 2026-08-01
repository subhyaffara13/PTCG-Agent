
def _get_memory_space_and_raise_if_hbm(aval, primitive_name, message=None):
  memory_space = _forward_any_to_hbm(aval.memory_space)
  if memory_space is _HBM:
    if message is None:
      message = (
          f'{primitive_name}: Buffers with a memory space of HBM or ANY cannot'
          ' be referenced directly. Instead, use `pltpu.sync_copy` or'
          ' `pltpu.async_copy`.'
      )
    raise ValueError(message)
  return memory_space

