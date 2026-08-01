
def create_hooks_from_stubs(concrete_type, hook_stubs, pre_hook_stubs) -> None:
    hook_defs = [h.def_ for h in hook_stubs]
    hook_rcbs = [h.resolution_callback for h in hook_stubs]

    pre_hook_defs = [h.def_ for h in pre_hook_stubs]
    pre_hook_rcbs = [h.resolution_callback for h in pre_hook_stubs]

    concrete_type._create_hooks(hook_defs, hook_rcbs, pre_hook_defs, pre_hook_rcbs)

