
def _logger_reduce(obj):
    return logging.getLogger, (obj.name,)

