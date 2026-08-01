
def register_log(setting_name, log_name) -> None:
    """
    Enables a log to be controlled by the env var and user API with the setting_name
    Args:
        setting_name:  the shorthand name used in the env var and user API
        log_name:  the log name that the setting_name is associated with
    """
    log_registry.register_log(setting_name, log_name)

