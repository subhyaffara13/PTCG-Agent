
def _remove_extraneous_pytrees(gm: torch.fx.GraphModule) -> None:
    """
    Remove extraneous pytree flatten/unflatten calls.

    We try a couple of optimizations here:
        1. Remove pytree flatten/unflatten calls between modules
        2. TODO: Remove module's in_spec + initial unflatten call
        3. TODO: Remove module's out_spec + final flatten call
    """

    for node in gm.graph.nodes:
        if node.op == "call_module" and node.target != "_guards_fn":
            _try_remove_connecting_pytrees(node)

    gm.graph.eliminate_dead_code()

