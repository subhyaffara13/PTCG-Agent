
def error_default_and_default_factory_specified(api: CheckerPluginInterface, context: Context) -> None:
    api.fail('Field default and default_factory cannot be specified together', context, code=ERROR_FIELD_DEFAULTS)

