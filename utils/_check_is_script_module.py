
def _check_is_script_module(model):
    if not isinstance(model, torch.jit.ScriptModule):
        raise ValueError("input must be a script module, got: " + str(type(model)))

