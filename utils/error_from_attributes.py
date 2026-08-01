
def error_from_attributes(model_name: str, api: CheckerPluginInterface, context: Context) -> None:
    """Emits an error when the model does not have `from_attributes=True`."""
    api.fail(f'"{model_name}" does not have from_attributes=True', context, code=ERROR_ORM)

