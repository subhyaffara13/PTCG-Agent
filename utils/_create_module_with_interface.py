
def _create_module_with_interface(
    module_cls, args, kwargs, device, module_interface_cls
):
    module = _create_module(module_cls, args, kwargs, device)
    if module_interface_cls is not None:
        module = torch.jit.script(module)
    return rpc.RRef(module, module_interface_cls)

