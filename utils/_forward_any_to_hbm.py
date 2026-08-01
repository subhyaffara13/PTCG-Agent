
def _forward_any_to_hbm(memory_space):
  if memory_space is _ANY:
    return _HBM
  return memory_space

