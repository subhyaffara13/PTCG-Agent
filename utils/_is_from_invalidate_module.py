
def _is_from_invalidate_module(exc: Exception) -> bool:
  """Check whether the exception is from an invalidated module."""
  tb = exc.__traceback__
  while tb is not None:
    frame = tb.tb_frame
    if '__etils_invalidated__' in frame.f_globals:
      return True
    tb = tb.tb_next

  return False

