
def init_test_logger() -> logging.Logger:
    """Initialize a test-specific logger with colored stderr handler and INFO level for tests.

    Uses a named logger instead of root logger to avoid conflicts with pytest-xdist parallel execution.
    Uses stderr instead of stdout to avoid deadlocks with pytest-xdist output capture.
    """
    logger = logging.getLogger("transformers.training_test")
    logger.setLevel(logging.INFO)

    # Only add handler if not already present (avoid duplicate handlers on repeated calls)
    if not logger.handlers:
        # Use stderr instead of stdout - pytest-xdist captures stdout which can cause deadlocks
        ch = logging.StreamHandler(sys.stderr)
        ch.setLevel(logging.INFO)

        # Use colored formatter if terminal supports it, plain otherwise
        if sys.stderr.isatty():
            formatter = ColoredFormatter(datefmt="%Y-%m-%d %H:%M:%S")
        else:
            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
            )

        ch.setFormatter(formatter)
        logger.addHandler(ch)

    logger.propagate = False  # Don't propagate to root logger to avoid duplicate output
    return logger

