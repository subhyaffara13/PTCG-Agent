
def _not_warning(record):
    return record.levelno < logging.WARNING


def _not_warning(record: logging.LogRecord) -> bool:
    return record.levelno < logging.WARNING

