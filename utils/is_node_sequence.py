
def is_node_sequence(
    nodes: Sequence[IRNode | Sequence[IRNode]],
) -> TypeIs[Sequence[IRNode]]:
    return all(isinstance(n, IRNode) for n in nodes)

