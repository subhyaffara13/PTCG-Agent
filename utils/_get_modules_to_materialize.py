
def _get_modules_to_materialize(
    root_module: nn.Module, ignored_modules: set[nn.Module]
) -> list[nn.Module]:
    # Run BFS to collect the modules to materialize via `reset_parameters()`,
    # stopping at any module with FSDP already applied or at ignored modules.
    modules_to_materialize: list[nn.Module] = []
    queue = collections.deque([root_module])
    visited_modules: set[nn.Module] = {root_module}
    while queue:
        module = queue.popleft()
        modules_to_materialize.append(module)
        for child_module in module.children():
            if (
                child_module not in visited_modules
                and _get_module_fsdp_state(child_module) is None
                and child_module not in ignored_modules
            ):
                visited_modules.add(child_module)
                queue.append(child_module)
    return modules_to_materialize

