from typing import Callable

def sequential_split(
    gm: torch.fx.GraphModule,
    node_call_back: Callable[[torch.fx.Node], torch.fx.Node | bool],
) -> torch.fx.GraphModule:
    """
    sequential_split creates a new graph module that splits the input graph module into multiple submodules
    based on the node_call_back. It doesn't mutate the input graph module. The node_call_back should return
    True if the node is a delimiter.  Delimiter will be the first node in the next submodule.
    """
    from torch.fx.passes.split_module import split_module

    split_map = {}
    split_id = 0
    for node in gm.graph.nodes:
        if node_call_back(node):
            split_id += 1
        split_map[node] = split_id

    new_gm = split_module(
        gm,
        gm,
        lambda node: split_map[node],
        keep_original_order=True,
        keep_original_node_name=True,
    )
    # Keep the codegen from original graph module to preserve e.g. pytree info.
    new_gm.graph._codegen = gm.graph._codegen
    new_gm.recompile()
    return new_gm

