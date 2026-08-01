
def _maybe_get_fqn(node: Node, gm: GraphModule) -> str | None:
    fqn = None
    if hasattr(gm, "_node_name_to_scope"):
        # fqn on observers is not present, because they do not
        # exist when the fqns are created during tracing. If this is
        # an observer, get the fqn of the node being observed.
        node_to_use_for_fqn = node
        if node.op == "call_module":
            if not isinstance(node.target, str):
                raise AssertionError(f"Expected str, got {type(node.target)}")
            module = getattr_from_fqn(gm, node.target)
            if _is_activation_post_process(module):
                node_to_use_for_fqn = get_normalized_nth_input(node, gm, 0)
        fqn = gm._node_name_to_scope[node_to_use_for_fqn.name][0]  # type: ignore[index]
    return fqn  # type: ignore[return-value]

