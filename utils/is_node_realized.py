
def is_node_realized(node: torch.fx.Node) -> bool:
    """Returns true if a node is always realized when lowered to inductor IR.

    NOTE: This may return some false negatives. e.g. it doesn't
    handle buffers realized heuristically during lowering, or
    buffers realized indirectly through view ops.
    """
    from torch._inductor.lowering import fallbacks, needs_realized_inputs

    def is_buffer(node: torch.fx.Node) -> bool:
        if node.op == "call_function" and node.target is operator.getitem:
            # For nodes with multiple outputs, we get the fx graph:
            #     foo = torch.ops.aten.foo(...)
            #     getitem = foo[0]
            #     getitem_1 = foo[1]
            # where we need to check if foo is a fallback kernel
            return is_buffer(node.args[0])  # type: ignore[arg-type]
        return node.op in ("placeholder", "output") or node.target in fallbacks

    if is_buffer(node):
        return True

    def realizes_inputs(node: torch.fx.Node) -> bool:
        return node.op == "output" or node.target in needs_realized_inputs

    if any(realizes_inputs(user) for user in node.users):
        return True

    # Otherwise, assume node isn't realized
    return False

