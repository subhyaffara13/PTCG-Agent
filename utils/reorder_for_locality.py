
def reorder_for_locality(graph: torch.fx.Graph):
    if torch.distributed.is_available():

        def check():
            # This is a wait node, and `other_node`` is some collective node.
            # Eager semantics allow waits to be issued in a different order than
            # the collectives. Reordering this wait node might reorder collectives
            # which cause hangs. Once we have SPMD mode, we can safely reorder them.
            # However, increasing the locality between a collective and its wait node
            # is generally worse for performance.
            return node.target != torch.ops._c10d_functional.wait_tensor.default
    else:

        def check():
            return True

    def consumes_rng_state(node: torch.fx.Node) -> bool:
        return (
            node.op == "call_function"
            and isinstance(node.target, torch._ops.OpOverload)
            and torch.Tag.nondeterministic_seeded in node.target.tags
        )

    def visit(other_node):
        if (
            other_node.op == "call_function"
            and other_node.target != operator.getitem
            and all((n in seen_nodes) for n in other_node.users)
            and get_mutation_region_id(graph, node)
            == get_mutation_region_id(graph, other_node)
            and check()
        ):
            # Ops that consume RNG state are order-sensitive and must not be
            # reordered during locality optimization.
            if consumes_rng_state(other_node):
                return

            # move node's producers right before it
            node.prepend(other_node)

    seen_nodes = OrderedSet[torch.fx.Node]()

    # only reorder nodes before the first copy_ in the graph.
    # copy_ will appear at the end of functionalized graphs when there is mutation on inputs,
    # and this reordering doesn't work well with mutation
    first_copy = next(
        iter(graph.find_nodes(op="call_function", target=torch.ops.aten.copy_.default)),
        None,
    )
    past_mutating_epilogue = first_copy is None

    for node in reversed(graph.nodes):
        seen_nodes.add(node)
        if not past_mutating_epilogue:
            past_mutating_epilogue = node is first_copy
            continue

        torch.fx.map_arg((node.args, node.kwargs), visit)

