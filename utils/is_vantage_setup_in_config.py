
def is_vantage_setup_in_config() -> bool:
    """Check if Vantage is setup in config.yaml, environment variables, or programmatically."""
    from litellm.integrations.vantage.vantage_logger import VantageLogger

    for cb in litellm.callbacks:
        if cb == "vantage" or isinstance(cb, VantageLogger):
            return True
    return False

