
def nn_module_has_global_hooks() -> bool:
    # This is limited to backward hooks for now because NNModuleVariable
    # supports fwd hooks underneath.
    return bool(
        len(torch.nn.modules.module._global_backward_hooks)
        or len(torch.nn.modules.module._global_backward_pre_hooks)
    )

