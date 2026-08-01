
def _get_root_modules(modules: list[nn.Module]) -> list[nn.Module]:
    """
    Returns the modules in ``modules`` that are root modules (i.e.
    parent-less) with respect to the set ``modules``. In other words, these
    are the modules in ``modules`` that are the not child of any other
    module in ``modules``.
    """
    root_modules: list[nn.Module] = []
    module_to_modules: dict[nn.Module, set[nn.Module]] = {
        module: set(module.modules()) for module in modules
    }
    for candidate_module in modules:
        is_root_module = True
        for module, _modules in module_to_modules.items():
            is_child_module = (
                candidate_module is not module and candidate_module in _modules
            )
            if is_child_module:
                is_root_module = False
                break
        if is_root_module:
            root_modules.append(candidate_module)
    return root_modules


def _get_root_modules(modules: set[nn.Module]) -> set[nn.Module]:
    """
    Returns:
        Set[nn.Module]: The subset of ``modules`` that are root modules (i.e.
        parent-less) with respect to the modules in the set itself. In other
        words, these are the modules in ``modules`` that are not the child of
        any other module in ``modules``.
    """
    root_modules: set[nn.Module] = set()
    module_to_submodules = {module: set(module.modules()) for module in modules}
    for candidate_module in modules:
        is_root_module = True
        for module, submodules in module_to_submodules.items():
            is_child_module = (
                candidate_module is not module and candidate_module in submodules
            )
            if is_child_module:
                is_root_module = False
                break
        if is_root_module:
            root_modules.add(candidate_module)
    return root_modules

