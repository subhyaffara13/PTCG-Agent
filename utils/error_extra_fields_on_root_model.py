
def error_extra_fields_on_root_model(api: CheckerPluginInterface, context: Context) -> None:
    """Emits an error when there is more than just a root field defined for a subclass of RootModel."""
    api.fail('Only `root` is allowed as a field of a `RootModel`', context, code=ERROR_EXTRA_FIELD_ROOT_MODEL)

