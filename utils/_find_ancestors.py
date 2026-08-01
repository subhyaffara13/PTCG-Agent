
def _find_ancestors(node: torch.fx.Node) -> OrderedSet[torch.fx.Node]:
    ancestors = OrderedSet[torch.fx.Node]()
    ancestors.add(node)
    cur_nodes = [node]
    while len(cur_nodes) > 0:
        new_nodes = []
        for node in cur_nodes:
            for inp in node.all_input_nodes:
                if inp not in ancestors:
                    ancestors.add(inp)
                    new_nodes.append(inp)
        cur_nodes = new_nodes
    return OrderedSet(node for node in ancestors if node.op != "placeholder")

