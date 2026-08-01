
def _init_script_module() -> "ScriptModule":
    import torch.jit

    return torch.jit.ScriptModule()

