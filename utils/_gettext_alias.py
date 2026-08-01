
def _gettext_alias(
    __context: Context, *args: t.Any, **kwargs: t.Any
) -> t.Union[t.Any, Undefined]:
    return __context.call(__context.resolve("gettext"), *args, **kwargs)

