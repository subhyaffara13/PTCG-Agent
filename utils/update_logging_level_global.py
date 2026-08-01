
def update_logging_level_global(logging_level: str | None) -> None:
  # remove previous handlers
  for logger_name, level in _logging_level_set.items():
    logger = logging.getLogger(logger_name)
    logger.removeHandler(_jax_logger_handler)
    logger.setLevel(level)
  _logging_level_set.clear()
  _set_cpp_min_log_level(logging_level)

  if logging_level is None:
    return

  logging_level_num = _nameToLevel[logging_level]

  # update jax and jaxlib root loggers for propagation
  root_loggers = [logging.getLogger("jax"), logging.getLogger("jaxlib")]
  for logger in root_loggers:
    logger.setLevel(logging_level_num)
    if logging_level_num != logging.NOTSET:
      logger.addHandler(_jax_logger_handler)
    _logging_level_set[logger.name] = logger.level

