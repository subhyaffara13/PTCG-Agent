
def insert_quantized_node(
    gm: torch.fx.GraphModule,
    val_node: torch.fx.Node,
    scale_node: float | torch.fx.Node,
    zero_point_node: float | torch.fx.Node,
    qmin_node: float | int | torch.fx.Node,
    qmax_node: float | int | torch.fx.Node,
    dtype_node: torch.dtype | torch.fx.Node,
    qscheme: torch.qscheme | None,
) -> torch.fx.Node:
    return gm.graph.call_function(
        quantize_per_tensor,
        (
            val_node,
            scale_node,
            zero_point_node,
            qmin_node,
            qmax_node,
            dtype_node,
        ),
    )

