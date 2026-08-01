
def _filtering_mode() -> str:
  mode = config.traceback_filtering.value
  if mode is None or mode == "auto":
    if (_running_under_ipython() and _ipython_supports_tracebackhide()):
      mode = "tracebackhide"
    else:
      mode = "quiet_remove_frames"
  return mode

