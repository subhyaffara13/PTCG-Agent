import logging

def _enable_debug_logging(logger_name):
  """Makes the specified logger log everything to stderr.

  Also adds more useful debug information to the log messages, e.g. the time.

  Args:
    logger_name: the name of the logger, e.g. "jax._src.xla_bridge".
  """
  logger = logging.getLogger(logger_name)
  _debug_enabled_loggers.append((logger, logger.level))

  logger.addHandler(_debug_handler)
  logger.setLevel(logging.DEBUG)

