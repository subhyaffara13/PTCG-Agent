
def lookup_target(
    manager: BuildManager, target: str, module_id: str
) -> tuple[list[FineGrainedDeferredNode], TypeInfo | None]:
    """Look up a target by fully-qualified name.

    The first item in the return tuple is a list of deferred nodes that
    needs to be reprocessed. If the target represents a TypeInfo corresponding
    to a protocol, return it as a second item in the return tuple, otherwise None.
    """
    deferred, stale_proto = _lookup_target_impl(manager, target)

    # If there are function targets that can infer outer variables, they should
    # be re-processed as part of the module top-level instead (for consistency).
    regular = []
    shared = []
    for d in deferred:
        if isinstance(d.node, FuncBase) and d.node.def_or_infer_vars:
            shared.append(d)
        else:
            regular.append(d)
    deferred = regular
    if shared:
        deferred.append(FineGrainedDeferredNode(manager.modules[module_id], None))
    return deferred, stale_proto

