
def _check_graph_equivalence(x: torch.nn.Module, y: torch.nn.Module):
    def graph_dump(graph: torch.fx.Graph) -> str:
        ret = []
        nodes_idx: dict[int, int] = {}

        def arg_dump(arg) -> str:
            if isinstance(arg, torch.fx.Node):
                return "%" + str(nodes_idx[id(arg)])
            return str(arg)

        for i, node in enumerate(graph.nodes):
            args_dump = [str(arg) for arg in pytree.tree_map(arg_dump, node.args)]
            args_dump += [
                f"{key}={value}"
                for key, value in pytree.tree_map(arg_dump, node.kwargs).items()
            ]
            target = node.target if node.op in ("call_function", "get_attr") else ""
            # pyrefly: ignore [bad-argument-type]
            ret.append(f"{i}: {node.op}[{target}]({', '.join(args_dump)})")
            nodes_idx[id(node)] = i
        return "\n".join(ret)

    if not isinstance(x.graph, torch.fx.Graph):
        raise AssertionError(
            f"expected x.graph to be torch.fx.Graph, got {type(x.graph)}"
        )
    if not isinstance(y.graph, torch.fx.Graph):
        raise AssertionError(
            f"expected y.graph to be torch.fx.Graph, got {type(y.graph)}"
        )
    return graph_dump(x.graph) == graph_dump(y.graph)

