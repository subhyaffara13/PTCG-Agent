
def _set_cpp_min_log_level(logging_level: str | None = None):
  if logging_level in (None, "NOTSET"):
    return
  # set cpp runtime logging level if the level is anything but NOTSET
  if logging_level not in _tf_cpp_map:
    raise ValueError(f"Attempting to set log level \"{logging_level}\" which"
                      f" isn't one of the supported:"
                      f" {list(_tf_cpp_map.keys())}.")
  # config the CPP logging level 0 - debug, 1 - info, 2 - warning, 3 - error
  log_level = _tf_cpp_map[logging_level]
  utils.absl_set_min_log_level(log_level)

