
def _collect_placeholder_nodes(var: "VariableTracker") -> list[torch.fx.Node]:
    """Recursively collect FX placeholder nodes from a VariableTracker.

    The returned placeholder nodes carry grapharg.example (real tensor) and
    example_value (FakeTensor) metadata — comparing these reveals lost
    autograd linkage (e.g., grad_fn dropped during tracing).
    See NOTE [Detecting lost autograd linkage in closure-captured tensors].
    """
    from .lazy import LazyVariableTracker
    from .lists import BaseListVariable
    from .tensor import TensorVariable

    result: list[torch.fx.Node] = []
    if isinstance(var, TensorVariable):
        node = var.as_proxy().node
        if node.op == "placeholder":
            result.append(node)
    elif isinstance(var, LazyVariableTracker):
        result.extend(_collect_placeholder_nodes(var.realize()))
    elif isinstance(var, BaseListVariable):
        for item in var.items:
            result.extend(_collect_placeholder_nodes(item))
    else:
        unimplemented(
            gb_type="_autograd_grad with unsupported argument type",
            context=f"got {type(var).__name__}",
            explanation=(
                f"_autograd_grad() received an argument of type {type(var).__name__} "
                "which is not supported. Expected tensor or sequence of tensors."
            ),
            hints=[
                "Ensure outputs and inputs arguments are tensors or sequences of tensors.",
            ],
        )
    return result

