
def nnmodule_has_hooks(
    mod: torch.nn.Module,
    check_forward_hooks: bool = False,
    check_backward_hooks: bool = False,
    check_state_dict_hooks: bool = False,
) -> bool:
    """
    Helper function to check if a module has any hooks attached to it.
    """
    hooks = nn_module_get_all_hooks(
        mod,
        check_forward_hooks=check_forward_hooks,
        check_backward_hooks=check_backward_hooks,
        check_state_dict_hooks=check_state_dict_hooks,
    )
    return bool(hooks)

