
def _is_absl_fatal_record(log_record):
  return (log_record.levelno >= logging.FATAL and
          log_record.__dict__.get(_ABSL_LOG_FATAL, False))

