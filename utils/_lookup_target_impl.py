
def _lookup_target_impl(
    manager: BuildManager, target: str
) -> tuple[list[FineGrainedDeferredNode], TypeInfo | None]:
    def not_found() -> None:
        manager.log_fine_grained(f"Can't find matching target for {target} (stale dependency?)")

    modules = manager.modules
    items = split_target(modules, target)
    if items is None:
        not_found()  # Stale dependency
        return [], None
    module, rest = items
    if rest:
        components = rest.split(".")
    else:
        components = []
    node: SymbolNode | None = modules[module]
    file: MypyFile | None = None
    active_class = None
    for c in components:
        if isinstance(node, TypeInfo):
            active_class = node
        if isinstance(node, MypyFile):
            file = node
        if not isinstance(node, (MypyFile, TypeInfo)) or c not in node.names:
            not_found()  # Stale dependency
            return [], None
        # Don't reprocess plugin generated targets. They should get
        # stripped and regenerated when the containing target is
        # reprocessed.
        if node.names[c].plugin_generated:
            return [], None
        node = node.names[c].node
    if isinstance(node, TypeInfo):
        # A ClassDef target covers the body of the class and everything defined
        # within it.  To get the body we include the entire surrounding target,
        # typically a module top-level, since we don't support processing class
        # bodies as separate entities for simplicity.
        assert file is not None
        if node.fullname != target:
            # This is a reference to a different TypeInfo, likely due to a stale dependency.
            # Processing them would spell trouble -- for example, we could be refreshing
            # a deserialized TypeInfo with missing attributes.
            not_found()
            return [], None
        result = [FineGrainedDeferredNode(file, None)]
        stale_info: TypeInfo | None = None
        if node.is_protocol:
            stale_info = node
        for name, symnode in node.names.items():
            node = symnode.node
            if isinstance(node, FuncDef):
                method, _ = _lookup_target_impl(manager, target + "." + name)
                result.extend(method)
        return result, stale_info
    if isinstance(node, Decorator):
        # Decorator targets actually refer to the function definition only.
        node = node.func
    if not isinstance(node, (FuncDef, MypyFile, OverloadedFuncDef)):
        # The target can't be refreshed. It's possible that the target was
        # changed to another type and we have a stale dependency pointing to it.
        not_found()
        return [], None
    if node.fullname != target:
        # Stale reference points to something unexpected. We shouldn't process since the
        # context will be wrong and it could be a partially initialized deserialized node.
        not_found()
        return [], None
    return [FineGrainedDeferredNode(node, active_class)], None

