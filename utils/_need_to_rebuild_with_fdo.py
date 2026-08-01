
def _need_to_rebuild_with_fdo(pgle_profiler):
  return (pgle_profiler is not None and pgle_profiler.is_enabled()
          and not pgle_profiler.is_fdo_consumed())

