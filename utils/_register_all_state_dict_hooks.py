
def _register_all_state_dict_hooks(state: _FSDPState):
    """
    Registers pre-save, post-save, pre-load, and post-load state dict hooks.
    """
    for hook_registration_fn_str, hook, hook_registration_fn_kwargs in (
        ("register_state_dict_pre_hook", _pre_state_dict_hook, {}),
        ("_register_state_dict_hook", _post_state_dict_hook, {}),
        (
            "_register_load_state_dict_pre_hook",
            _pre_load_state_dict_hook,
            {"with_module": True},
        ),
        ("register_load_state_dict_post_hook", _post_load_state_dict_hook, {}),
    ):
        _register_state_dict_hooks_base(
            state, hook_registration_fn_str, hook, hook_registration_fn_kwargs
        )

