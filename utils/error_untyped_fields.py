
def error_untyped_fields(api: SemanticAnalyzerPluginInterface, context: Context) -> None:
    """Emits an error when there is an untyped field in the model."""
    api.fail('Untyped fields disallowed', context, code=ERROR_UNTYPED)


def error_untyped_fields(api: SemanticAnalyzerPluginInterface, context: Context) -> None:
    api.fail('Untyped fields disallowed', context, code=ERROR_UNTYPED)

