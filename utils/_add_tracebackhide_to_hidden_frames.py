
def _add_tracebackhide_to_hidden_frames(tb: types.TracebackType | None):
  if tb is None:
    return
  for f, _lineno in traceback.walk_tb(tb):
    if not include_frame(f) and not _is_reraiser_frame(f):
      f.f_locals["__tracebackhide__"] = True

