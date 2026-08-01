
def _detailed_list(
    mgr: extension.ExtensionManager[T],
    over: str = '',
    under: str = '-',
    titlecase: bool = False,
) -> Iterable[tuple[str, str]]:
    for name in sorted(mgr.names()):
        ext = mgr[name]
        if over:
            yield (over * len(ext.name), ext.module_name)
        if titlecase:
            yield (ext.name.title(), ext.module_name)
        else:
            yield (ext.name, ext.module_name)
        if under:
            yield (under * len(ext.name), ext.module_name)
        yield ('\n', ext.module_name)
        doc = _get_docstring(ext.plugin)
        if doc:
            yield (doc, ext.module_name)
        else:
            yield (
                f'.. warning:: No documentation found for {ext.name} in '
                f'{ext.entry_point_target}',
                ext.module_name,
            )
        yield ('\n', ext.module_name)

