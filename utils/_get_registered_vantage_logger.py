
def _get_registered_vantage_logger():
    """Return the VantageLogger already registered in litellm.callbacks, if any."""
    from litellm.integrations.vantage.vantage_logger import VantageLogger

    vantage_loggers = litellm.logging_callback_manager.get_custom_loggers_for_type(
        callback_type=VantageLogger
    )
    if vantage_loggers:
        return vantage_loggers[0]
    return None

