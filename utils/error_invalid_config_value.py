
def error_invalid_config_value(name: str, api: SemanticAnalyzerPluginInterface, context: Context) -> None:
    """Emits an error when the config value is invalid."""
    api.fail(f'Invalid value for "Config.{name}"', context, code=ERROR_CONFIG)


def error_invalid_config_value(name: str, api: SemanticAnalyzerPluginInterface, context: Context) -> None:
    api.fail(f'Invalid value for "Config.{name}"', context, code=ERROR_CONFIG)

