
def is_cudagraph_unsafe_op(node: Operation) -> bool:
    """
    Returns True if the node is an op that is not cudagraphable.
    This includes:
    - Ops in FORBIDDEN_CUDAGRAPH_OPS (CPU sync, dynamic alloc, etc.)
    - Ops with the cudagraph_unsafe tag
    - index_put_ with boolean indices (triggers .nonzero() during capture)
    - Control flow nodes (Conditional, WhileLoop)
    - Ops with sparse tensor outputs
    """
    from . import ir

    # Control flow nodes are cudagraph-unsafe
    if isinstance(node, (ir.Conditional, ir.WhileLoop)):
        return True

    if not isinstance(node, (ir.FallbackKernel, ir.ExternKernel)):
        return False

    fx_node = getattr(node, "fx_node", None)
    if fx_node is not None and is_cudagraph_unsafe_fx_node(fx_node):
        return True

    return False

