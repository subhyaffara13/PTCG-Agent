
def tangent_has_chunking_meta(gm: GraphModule) -> bool:
    from .core import get_chunking_meta

    return any(
        is_tangent_node(node) and get_chunking_meta(node) is not None
        for node in gm.graph.find_nodes(op="placeholder", sort=False)
    )

