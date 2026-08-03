from typing import Any

def inline_subgraph_to_ir_nodes(
    gm: torch.fx.GraphModule, inputs: list[Any], name: str
) -> Any:
    """Inline a subgraph by converting its FX operations to individual IR nodes.

    This converts a subgraph to multiple ComputedBuffer nodes (fusable),
    enabling epilogue fusion with subsequent operations.

    Returns:
        TensorBox containing the final operation result as individual IR nodes
    """
    from torch._inductor.lowering import process_subgraph_nodes

    # Temporarily switch V.graph.module to subgraph during processing; restore to prevent IR nodes added to wrong graph
    original_module = V.graph.module
    try:
        V.graph.module = gm
        return process_subgraph_nodes(gm, inputs)
    finally:
        V.graph.module = original_module

