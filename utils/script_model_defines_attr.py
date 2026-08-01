
def script_model_defines_attr(script_model, attr):
    script_attr = getattr(script_model, attr, None)
    if script_attr is None:
        return False
    default_attr = getattr(torch.jit.RecursiveScriptModule, attr, None)
    if default_attr is None:
        return False
    return script_attr != default_attr

