
def _is_script_method(module: object) -> TypeIs["ScriptMethod"]:
    import torch.jit

    return isinstance(module, torch._C.ScriptMethod)

