import logging

def _is_non_absl_fatal_record(log_record):
  return (log_record.levelno >= logging.FATAL and
          not log_record.__dict__.get(_ABSL_LOG_FATAL, False))

