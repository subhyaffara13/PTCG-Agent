
def _is_attr_overridden(
    tx: "InstructionTranslator", var: VariableTracker, name: str
) -> bool:
    if not isinstance(var, (TensorWithTFOverrideVariable, UserDefinedObjectVariable)):
        return False
    import torch

    overridden = False
    try:
        attr_val = inspect.getattr_static(var.python_type(), name)
        overridden |= attr_val != getattr(torch.Tensor, name)
    except AttributeError:
        pass

    return overridden

