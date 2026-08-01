
def delete_module(module_id: str, path: str, graph: Graph, manager: BuildManager) -> None:
    manager.log_fine_grained(f"delete module {module_id!r}")
    # TODO: Remove deps for the module (this only affects memory use, not correctness)
    if module_id in graph:
        del graph[module_id]
    if module_id in manager.modules:
        del manager.modules[module_id]
    components = module_id.split(".")
    if len(components) > 1:
        # Delete reference to module in parent module.
        parent_id = ".".join(components[:-1])
        # If parent module is ignored, it won't be included in the modules dictionary.
        if parent_id in manager.modules:
            parent = manager.modules[parent_id]
            if components[-1] in parent.names:
                del parent.names[components[-1]]
    # If the module is removed from the build but still exists, then
    # we mark it as missing so that it will get picked up by import from still.
    if manager.fscache.isfile(path):
        # TODO: check if there is an equivalent of #20800 for the daemon.
        manager.missing_modules[module_id] = SuppressionReason.NOT_FOUND

