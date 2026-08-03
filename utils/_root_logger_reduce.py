import logging

def _root_logger_reduce(obj):
    return logging.getLogger, ()

