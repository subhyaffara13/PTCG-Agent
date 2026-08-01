
def get_timeout_config_value(config: Config) -> float:
    return float(config.getini("faulthandler_timeout") or 0.0)

