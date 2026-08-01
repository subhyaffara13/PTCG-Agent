
def _update_transfer_guard(state, key, val):
  """Applies the transfer guard level within guard_lib."""
  if val is None:
    setattr(state, key, None)
  elif val == 'allow':
    setattr(state, key, guard_lib.TransferGuardLevel.ALLOW)
  elif val == 'log':
    setattr(state, key, guard_lib.TransferGuardLevel.LOG)
  elif val == 'disallow':
    setattr(state, key, guard_lib.TransferGuardLevel.DISALLOW)
  elif val == 'log_explicit':
    setattr(state, key, guard_lib.TransferGuardLevel.LOG_EXPLICIT)
  elif val == 'disallow_explicit':
    setattr(state, key, guard_lib.TransferGuardLevel.DISALLOW_EXPLICIT)
  else:
    assert False, f'Invalid transfer guard level {val}'

