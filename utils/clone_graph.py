
def clone_graph(input_graph: torch.fx.GraphModule) -> torch.fx.GraphModule:
    class CopyGraph(Transformer):
        def run_node(self, old_node: torch.fx.Node) -> torch.fx.Node:
            new_node = super().run_node(old_node)
            if isinstance(new_node, torch.fx.Proxy):
                new_node.node.meta.update(old_node.meta)
                new_node.node.name = self.new_graph._graph_namespace.create_name(
                    old_node.name, None
                )

            return new_node

    return CopyGraph(input_graph).transform()

