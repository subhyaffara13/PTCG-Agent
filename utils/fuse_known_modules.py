
def fuse_known_modules(mod_list, is_qat, additional_fuser_method_mapping=None):
    r"""Return a list of known fuse modules.

    Returns a list of modules that fuses the operations specified
     in the input module list.

    Fuses only the following sequence of modules:
    conv, bn
    conv, bn, relu
    conv, relu
    linear, bn
    linear, relu
    For these sequences, the first element in the output module list performs
    the fused operation. The rest of the elements are set to nn.Identity()
    """
    types = tuple(type_before_parametrizations(m) for m in mod_list)
    fuser_method = get_fuser_method(types, additional_fuser_method_mapping)
    if fuser_method is None:
        raise NotImplementedError(f"Cannot fuse modules: {types}")
    new_mod: list[nn.Module | None] = [None] * len(mod_list)
    fused = fuser_method(is_qat, *mod_list)
    # NOTE: forward hooks not processed in the two following for loops will be lost after the fusion
    # Move pre forward hooks of the base module to resulting fused module
    for pre_hook_fn in mod_list[0]._forward_pre_hooks.values():
        fused.register_forward_pre_hook(pre_hook_fn)
    mod_list[0]._forward_pre_hooks.clear()
    # Move post forward hooks of the last module to resulting fused module
    for hook_fn in mod_list[-1]._forward_hooks.values():
        fused.register_forward_hook(hook_fn)
    mod_list[-1]._forward_hooks.clear()
    new_mod[0] = fused

    for i in range(1, len(mod_list)):
        identity = nn.Identity()
        identity.training = mod_list[0].training
        new_mod[i] = identity

    return new_mod

