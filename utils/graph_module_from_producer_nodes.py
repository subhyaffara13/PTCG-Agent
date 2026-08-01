
def graph_module_from_producer_nodes(
    root: GraphModule, producer_nodes: list[Node]
) -> GraphModule:
    r"""Construct a graph module from extracted producer nodes
    from `collect_producer_nodes` function
    Args:
      root: the root module for the original graph
      producer_nodes: a list of nodes we use to construct the graph
    Return:
      A graph module constructed from the producer nodes
    """
    if len(producer_nodes) == 0:
        raise AssertionError("list of producer nodes can not be empty")
    # since we traced back from node to getattr
    producer_nodes.reverse()
    graph = Graph()
    env: dict[Any, Any] = {}

    def load_arg(a):
        return map_arg(a, lambda node: env[node])

    for producer_node in producer_nodes:
        env[producer_node] = graph.node_copy(producer_node, load_arg)
    graph.output(load_arg(producer_nodes[-1]))
    graph_module = GraphModule(root, graph)
    return graph_module

