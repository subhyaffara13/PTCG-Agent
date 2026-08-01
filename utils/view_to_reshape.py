
def view_to_reshape(gm):
    """
    Replace view ops in the GraphModule to reshape ops.
    """

    def _view_to_reshape_graph(graph):
        for nd in graph.find_nodes(
            op="call_function", target=torch.ops.aten.view.default
        ):
            nd.target = torch.ops.aten.reshape.default

    def _recursive_view_to_reshape(graph):
        apply_pass_to_subgraphs(_recursive_view_to_reshape, graph)
        _view_to_reshape_graph(graph)

    _recursive_view_to_reshape(gm.graph)

