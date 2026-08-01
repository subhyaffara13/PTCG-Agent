
def calculate_quantization_scaling(
    graph: torch.fx.Graph,
    node: torch.fx.Node,
    max: float = 57344.0,
    min: float = 1e-12,
    position: int = 0,
) -> torch.fx.Node:
    with graph.inserting_after(node):
        abs_node = graph.call_function(
            torch.ops.aten.abs.default,
            args=(node,),
        )
        abs_node.meta["val"] = torch.ops.aten.abs.default(node.meta["val"])
        abs_node.meta["tensor_meta"] = extract_tensor_metadata(abs_node.meta["val"])
    with graph.inserting_after(abs_node):
        amax_node = graph.call_function(
            torch.ops.aten.amax.default,
            args=(abs_node, [-1], True),
        )
        amax_node.meta["val"] = torch.ops.aten.amax.default(
            abs_node.meta["val"], [-1], True
        )
        amax_node.meta["tensor_meta"] = extract_tensor_metadata(amax_node.meta["val"])
    with graph.inserting_after(amax_node):
        amax_64_node = graph.call_function(
            torch.ops.prims.convert_element_type.default,
            args=(amax_node, torch.float64),
        )
        amax_64_node.meta["val"] = torch.ops.prims.convert_element_type.default(
            amax_node.meta["val"], torch.float64
        )
        amax_64_node.meta["tensor_meta"] = extract_tensor_metadata(
            amax_64_node.meta["val"]
        )
    with graph.inserting_after(amax_64_node):
        clamp_min_node = graph.call_function(
            torch.ops.aten.clamp_min.default,
            args=(amax_64_node, min),
        )
        clamp_min_node.meta["val"] = torch.ops.aten.clamp_min.default(
            amax_64_node.meta["val"], min
        )
        clamp_min_node.meta["tensor_meta"] = extract_tensor_metadata(
            clamp_min_node.meta["val"]
        )
    with graph.inserting_after(clamp_min_node):
        reciprocal_node = graph.call_function(
            torch.ops.aten.reciprocal.default,
            args=(clamp_min_node,),
        )
        reciprocal_node.meta["val"] = torch.ops.aten.reciprocal.default(
            clamp_min_node.meta["val"]
        )
        reciprocal_node.meta["tensor_meta"] = extract_tensor_metadata(
            reciprocal_node.meta["val"]
        )
    with graph.inserting_after(reciprocal_node):
        mul_node = graph.call_function(
            torch.ops.aten.mul.Tensor,
            args=(reciprocal_node, max),
        )
        mul_node.meta["val"] = torch.ops.aten.mul.Tensor(
            reciprocal_node.meta["val"], max
        )
        mul_node.meta["tensor_meta"] = extract_tensor_metadata(mul_node.meta["val"])
    with graph.inserting_after(mul_node):
        scale_node = graph.call_function(
            torch.ops.prims.convert_element_type.default,
            args=(mul_node, torch.float32),
            name=f"fp8_scale_pos_{position}_{node.name}",
        )
        scale_node.meta["val"] = torch.ops.prims.convert_element_type.default(
            mul_node.meta["val"], torch.float32
        )
        scale_node.meta["tensor_meta"] = extract_tensor_metadata(scale_node.meta["val"])
    return scale_node

