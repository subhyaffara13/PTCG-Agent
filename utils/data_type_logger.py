import logging

def data_type_logger(msg: str) -> None:
    if schedule_log.isEnabledFor(logging.DEBUG):
        schedule_log.debug("Data type propagation: %s", msg)

