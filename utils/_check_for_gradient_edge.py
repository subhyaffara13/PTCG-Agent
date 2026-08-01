
def _check_for_gradient_edge(var: VariableTracker, arg_name: str) -> None:
    """Check if var contains a GradientEdge from outside the compiled region.

    Used by handle_autograd_grad to reject external GradientEdge objects that
    cannot be traced through.
    """
    from .lists import BaseListVariable

    if isinstance(var, UserDefinedTupleVariable) and type(var.value) is GradientEdge:
        # Try to get source info for context
        source_info = var.source.name if var.source else None
        context = f"GradientEdge in {arg_name}"
        if source_info:
            context += f": {source_info}"

        unimplemented(
            gb_type="autograd.grad with external GradientEdge",
            context=context,
            explanation=(
                "torch.autograd.grad() cannot be used with GradientEdge inputs "
                "passed from outside the compiled region. The GradientEdge contains "
                "a reference to an autograd node that was created before torch.compile "
                "started tracing, so Dynamo cannot trace through its computation."
            ),
            hints=[
                "Move the autograd.grad() call outside the torch.compile region.",
                "Or use tensor inputs directly instead of GradientEdge objects.",
                *graph_break_hints.SUPPORTABLE,
            ],
        )
    elif isinstance(var, BaseListVariable):
        for i, item in enumerate(var.items):
            _check_for_gradient_edge(item, f"{arg_name}[{i}]")

