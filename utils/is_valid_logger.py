import logging

def is_valid_logger(logger: abstract_logger.AbstractLogger):
  if not isinstance(logger, abstract_logger.AbstractLogger):
    logging.warning(
        'CompositeLogger only supports AbstractLogger instances.'
    )
    return False
  if isinstance(logger, CompositeLogger):
    logging.warning(
        'CompositeLogger doesn\'t support instance of itself.'
    )
    return False
  return True

