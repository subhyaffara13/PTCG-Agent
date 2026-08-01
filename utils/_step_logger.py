
def _step_logger() -> Any:
    return torchdynamo_logging.get_step_logger(log)


def _step_logger() -> Callable[..., None]:
    return torchdynamo_logging.get_step_logger(log)


def _step_logger() -> Callable[..., None]:
    return dynamo_logging.get_step_logger(log)

