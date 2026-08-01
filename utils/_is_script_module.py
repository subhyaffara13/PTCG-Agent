
def _is_script_module(module: Module) -> TypeIs["ScriptModule"]:
    import torch.jit

    return isinstance(module, torch.jit.ScriptModule)

