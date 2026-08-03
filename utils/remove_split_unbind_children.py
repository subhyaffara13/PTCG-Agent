from typing import Any

def remove_split_unbind_children(graph: torch.fx.Graph, inputs: list[torch.fx.Node]):
    nodes = OrderedSet[Any]()
    for input in inputs:
        if input.target is operator.getitem:
            nodes.add(input.args[0])  # type: ignore[union-attr]
        if len(input.users.keys()) == 0:
            graph.erase_node(input)
    # check the split node to remove if it has no users
    for node in nodes:
        if len(node.users.keys()) == 0:  # type: ignore[union-attr]
            graph.erase_node(node)  # type: ignore[arg-type]

