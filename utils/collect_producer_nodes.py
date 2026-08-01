
def collect_producer_nodes(node: Node) -> list[Node] | None:
    r"""Starting from a target node, trace back until we hit input or
    getattr node. This is used to extract the chain of operators
    starting from getattr to the target node, for example::

        def forward(self, x):
            observed = self.observer(self.weight)
            return F.linear(x, observed)

    collect_producer_nodes(observed) will either return a list of nodes that
    produces the observed node or None if we can't extract a self contained
    graph without free variables(inputs of the forward function).
    """
    nodes = [node]
    frontier = [node]
    while frontier:
        node = frontier.pop()
        all_args = list(node.args) + list(node.kwargs.values())
        for arg in all_args:
            if not isinstance(arg, Node):
                continue
            if arg.op == "placeholder":
                # hit input, can't fold in this case
                return None
            nodes.append(arg)
            if not (arg.op == "call_function" and arg.target is getattr):
                frontier.append(arg)
    return nodes

