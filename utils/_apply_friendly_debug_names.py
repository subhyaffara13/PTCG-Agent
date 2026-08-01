
def _apply_friendly_debug_names(graph, params) -> None:
    for n in graph.nodes():
        for v in n.inputs():
            old_name = v.debugName()
            if old_name != str(v.unique()):
                continue
            new_name = f"{n.kind()}_{v.unique()}"
            v.setDebugName(new_name)
            if old_name in params:
                params[new_name] = params.pop(old_name)

