
def get_exit_on_timeout_config_value(config: Config) -> bool:
    exit_on_timeout = config.getini("faulthandler_exit_on_timeout")
    assert isinstance(exit_on_timeout, bool)
    return exit_on_timeout

