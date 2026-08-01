
def getattr_recursive(obj: Any, target: str) -> Any:
    target_atoms = target.split(".")
    attr_itr = obj
    for i, atom in enumerate(target_atoms):
        if not hasattr(attr_itr, atom):
            raise RuntimeError(
                f"Node referenced nonexistent target {'.'.join(target_atoms[:i])}"
            )
        attr_itr = getattr(attr_itr, atom)
    return attr_itr


def getattr_recursive(
    obj: GraphModule, target: str
) -> Tensor | torch._C.ScriptObject | GraphModule:
    target_atoms = target.split(".")
    attr_itr = obj
    for i, atom in enumerate(target_atoms):
        if not hasattr(attr_itr, atom):
            raise RuntimeError(
                f"Node referenced nonexistent target {'.'.join(target_atoms[:i])}"
            )
        attr_itr = getattr(attr_itr, atom)
    return attr_itr


def getattr_recursive(obj, name):
    for layer in name.split("."):
        if isinstance(obj, torch.nn.ModuleList):
            if hasattr(obj, "_modules") and layer in obj._modules:
                obj = obj._modules[layer]
            else:
                return None
        elif hasattr(obj, layer):
            obj = getattr(obj, layer)
        else:
            return None
    return obj

