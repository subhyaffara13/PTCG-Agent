
def _simple_list(
    mgr: extension.ExtensionManager[T],
) -> Iterable[tuple[str, str]]:
    for name in sorted(mgr.names()):
        ext = mgr[name]
        doc = _get_docstring(ext.plugin) or '\n'
        summary = doc.splitlines()[0].strip()
        yield (f'* {ext.name} -- {summary}', ext.module_name)

