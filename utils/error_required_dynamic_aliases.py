
def error_required_dynamic_aliases(api: SemanticAnalyzerPluginInterface, context: Context) -> None:
    """Emits required dynamic aliases error.

    This will be called when `warn_required_dynamic_aliases=True`.
    """
    api.fail('Required dynamic aliases disallowed', context, code=ERROR_ALIAS)


def error_required_dynamic_aliases(api: SemanticAnalyzerPluginInterface, context: Context) -> None:
    api.fail('Required dynamic aliases disallowed', context, code=ERROR_ALIAS)

