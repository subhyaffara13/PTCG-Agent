
def _should_skip_event(kwargs: Dict[str, Any]) -> bool:
    """Check if event should be skipped due to missing standard_logging_object."""
    if kwargs.get("standard_logging_object") is None:
        verbose_logger.debug(
            "OpikLogger skipping event; no standard_logging_object found"
        )
        return True
    return False

