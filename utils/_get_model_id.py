
def _get_model_id(obj) -> str | None:
    if isinstance(obj, torch.jit.ScriptModule):
        return str(obj._c._type())
    elif isinstance(obj, torch.jit.ScriptFunction):
        return obj.qualified_name
    else:
        return None

