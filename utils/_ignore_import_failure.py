
def _ignore_import_failure(
    node: ImportNode,
    modname: str,
    ignored_modules: Sequence[str],
) -> bool:
    if is_module_ignored(modname, ignored_modules):
        return True

    # Ignore import failure if part of guarded import block
    # I.e. `sys.version_info` or `typing.TYPE_CHECKING`
    if in_type_checking_block(node):
        return True
    if isinstance(node.parent, nodes.If) and is_sys_guard(node.parent):
        return True

    return node_ignores_exception(node, ImportError)

