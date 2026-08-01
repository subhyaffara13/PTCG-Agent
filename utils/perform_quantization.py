
def perform_quantization(
    graph: torch.fx.Graph,
    node: torch.fx.Node,
    scale_node: torch.fx.Node,
    quant_type: torch.dtype,
    clamp_min: float,
    clamp_max: float,
    position: int,
) -> torch.fx.Node:
    with graph.inserting_after(scale_node):
        target_node_32 = graph.call_function(
            torch.ops.prims.convert_element_type.default,
            args=(node, torch.float32),
        )
        target_node_32.meta["val"] = torch.ops.prims.convert_element_type.default(
            node.meta["val"], torch.float32
        )
        target_node_32.meta["tensor_meta"] = extract_tensor_metadata(
            target_node_32.meta["val"]
        )
    with graph.inserting_after(target_node_32):
        scaled_target_node = graph.call_function(
            torch.ops.aten.mul.Tensor,
            args=(target_node_32, scale_node),
        )
        scaled_target_node.meta["val"] = torch.ops.aten.mul.Tensor(
            target_node_32.meta["val"], scale_node.meta["val"]
        )
        scaled_target_node.meta["tensor_meta"] = extract_tensor_metadata(
            scaled_target_node.meta["val"]
        )
    with graph.inserting_after(scaled_target_node):
        clamp_min_scaled_node = graph.call_function(
            torch.ops.aten.clamp_min.default,
            args=(scaled_target_node, clamp_min),
        )
        clamp_min_scaled_node.meta["val"] = torch.ops.aten.clamp_min.default(
            scaled_target_node.meta["val"], clamp_min
        )
        clamp_min_scaled_node.meta["tensor_meta"] = extract_tensor_metadata(
            clamp_min_scaled_node.meta["val"]
        )
    with graph.inserting_after(clamp_min_scaled_node):
        clamp_max_scaled_node = graph.call_function(
            torch.ops.aten.clamp_max.default,
            args=(clamp_min_scaled_node, clamp_max),
        )
        clamp_max_scaled_node.meta["val"] = torch.ops.aten.clamp_max.default(
            clamp_min_scaled_node.meta["val"], clamp_max
        )
        clamp_max_scaled_node.meta["tensor_meta"] = extract_tensor_metadata(
            clamp_max_scaled_node.meta["val"]
        )
    with graph.inserting_after(clamp_max_scaled_node):
        quant_activation_node = graph.call_function(
            torch.ops.prims.convert_element_type.default,
            args=(clamp_max_scaled_node, quant_type),
            name=f"fp8_quant_pos_{position}_{node.name}",
        )
        quant_activation_node.meta["val"] = (
            torch.ops.prims.convert_element_type.default(
                clamp_max_scaled_node.meta["val"], quant_type
            )
        )
        quant_activation_node.meta["tensor_meta"] = extract_tensor_metadata(
            quant_activation_node.meta["val"]
        )
    return quant_activation_node

