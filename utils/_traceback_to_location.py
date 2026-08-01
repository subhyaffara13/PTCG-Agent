
def _traceback_to_location(ctx: HasTracebackCaches, tb: xc.Traceback) -> ir.Location:
  """Converts a full traceback to a callsite() MLIR location."""
  return ctx.traceback_caches.traceback_to_location_cache.get(tb)

