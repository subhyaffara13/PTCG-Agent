
def current() -> SourceInfo:
  source_info = _source_info_context.context
  if not source_info.traceback:
    source_info = source_info.replace(traceback=xla_client.Traceback.get_traceback())
  return source_info

