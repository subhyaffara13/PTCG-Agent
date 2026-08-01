
def replace_tracer_for_error_message(obj):
  # TODO(mattjj): Many ideas for improving this.  Crawl the stack and see if
  # there are user variables whose value is == to this object?  Or search
  # parameters of functions being transformed, at least?  Or at least assign
  # short unique ids to them?
  if isinstance(obj, Tracer):
    return SomeTracer()
  else:
    return obj

