
def invert_deps(deps: dict[str, set[str]], graph: Graph) -> dict[str, dict[str, set[str]]]:
    """Splits fine-grained dependencies based on the module of the trigger.

    Returns a dictionary from module ids to all dependencies on that
    module. Dependencies not associated with a module in the build will be
    associated with the nearest parent module that is in the build, or the
    fake module FAKE_ROOT_MODULE if none are.
    """
    # Lazy import to speed up startup
    from mypy.server.target import trigger_to_target

    # Prepopulate the map for all the modules that have been processed,
    # so that we always generate files for processed modules (even if
    # there aren't any dependencies to them.)
    rdeps: dict[str, dict[str, set[str]]] = {id: {} for id, st in graph.items() if st.tree}
    for trigger, targets in deps.items():
        module = module_prefix(graph, trigger_to_target(trigger))
        if not module or not graph[module].tree:
            module = FAKE_ROOT_MODULE

        mod_rdeps = rdeps.setdefault(module, {})
        mod_rdeps.setdefault(trigger, set()).update(targets)

    return rdeps

