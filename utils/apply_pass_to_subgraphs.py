from typing import Callable

def apply_pass_to_subgraphs(pass_fn: Callable[[fx.Graph], None], graph: fx.Graph):
    """Recursively apply a pass function to all subgraphs referenced by get_attr nodes."""
    gm = graph.owning_module
    if gm is None:
        return
    subgraph_names: OrderedSet[str] = OrderedSet(
        x.target for x in graph.find_nodes(op="get_attr")
    )
    for child_name, child_mod in gm.named_children():
        if child_name in subgraph_names and isinstance(child_mod, torch.fx.GraphModule):
            pass_fn(child_mod.graph)

