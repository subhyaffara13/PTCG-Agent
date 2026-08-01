
def with_checkpoint_logging(
    func: Callable | None = None,
    logger_name: str = "torch.distributed.checkpoint",
    level: int = logging.INFO,
) -> Callable | None:
    """
    Wrapper to configure checkpoint logging for distributed tests.

    Args:
        func: The test function to wrap
        logger_name: Name of the logger to configure (default: 'torch.distributed.checkpoint')
        level: Logging level to set (default: logging.INFO)
    """
    if func is None:
        raise AssertionError("Expected func to not be None")

    @wraps(func)
    def wrapper(self, *args: tuple[object], **kwargs: dict[str, Any]) -> None:
        # Get the logger and store original level
        target_logger = logging.getLogger(logger_name)
        original_level = target_logger.level

        # Set the desired logging level
        target_logger.setLevel(level)

        try:
            func(self, *args, **kwargs)
        finally:
            # Restore original logging level
            target_logger.setLevel(original_level)

    return wrapper

