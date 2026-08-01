
def remove_assert_ops(graph: torch.fx.Graph):
    """
    Removes aten._assert_tensor_metadata.default op because
    1) it will be lowered to a no-op in inductor
    2) it can block fusion, such as unfuse_bias_add_to_pointwise fusion.

    This op could come from aten.to functionalization in export.

    For example, if we have a graph like below

    %addmm = aten.addmm.default(%linear_bias, %arg3_1, %permute)
    %_assert_tensor_metadata = aten._assert_tensor_metadata.default(%addmm, None, None, torch.float16)
    %convert_element_type_3 = prims.convert_element_type.default(%addmm, torch.float32)
    %pow_1 = aten.pow.Tensor_Scalar(%convert_element_type_3, 2)

    We still want to fuse add from addmm with pow, instead of fusing add with mm, according to unfuse_bias_add_to_pointwise fusion.

    However, aten._assert_tensor_metadata.default is not a pointwise op, and would fail the should_prefer_unfused_addmm check.

    We remove this op so it doesn't block fusion decisions. It's safe because this op is lowered to a no-op with @register_lowering.

    """
    for node in graph.find_nodes(
        op="call_function", target=torch.ops.aten._assert_tensor_metadata.default
    ):
        graph.erase_node(node)

