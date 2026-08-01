
def _root_module_type(graph: torch.fx.Graph) -> str | None:
    for node in graph.nodes:
        if "nn_module_stack" not in node.meta:
            continue

        for path, ty in node.meta["nn_module_stack"].values():
            if not path:
                return ty
    return None

