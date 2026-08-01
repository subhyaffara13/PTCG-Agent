
def _update_garbage_collection_guard(state, key, val):
  """Applies the transfer guard level within guard_lib."""
  if val is None:
    setattr(state, key, None)
  elif val == 'allow':
    setattr(state, key, guard_lib.GarbageCollectionGuardLevel.ALLOW)
  elif val == 'log':
    setattr(state, key, guard_lib.GarbageCollectionGuardLevel.LOG)
  elif val == 'fatal':
    setattr(state, key, guard_lib.GarbageCollectionGuardLevel.FATAL)
  else:
    assert False, f'Invalid garbage collection guard level {val}'

