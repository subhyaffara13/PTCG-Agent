
def _get_module(model, submodule_key):
    tokens = submodule_key.split(".")
    cur_mod = model
    for s in tokens:
        cur_mod = getattr(cur_mod, s)
    return cur_mod


def _get_module(
    node: Node, named_modules: dict[str, torch.nn.Module]
) -> torch.nn.Module | None:
    """
    If `node` refers to a call_module node, return the module, else None.
    """
    if node.op == "call_module" and str(node.target) in named_modules:
        return named_modules[str(node.target)]
    else:
        return None


def _get_module(node: Node, modules: dict[str, nn.Module]) -> nn.Module | None:
    """
    Return the `torch.nn.Module` that corresponds to the specified node's target.
    If no such node exists, return None.
    """
    if node.op == "call_module" and str(node.target) in modules:
        return modules[str(node.target)]
    else:
        return None


def _get_module(target_name_prefix: str) -> Any:
  if target_name_prefix == "cu":
    return gpu_sparse._cusparse
  elif target_name_prefix == "hip":
    return gpu_sparse._hipsparse
  else:
    raise ValueError(f"Unsupported target_name_prefix: {target_name_prefix}")

