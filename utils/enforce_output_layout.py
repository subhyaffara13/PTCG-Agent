
def enforce_output_layout(gm: torch.fx.GraphModule):
    """
    Make sure the output node's layout does not change due to compiler optimizations
    by adding aten.as_strided nodes with the expected strides.

    Only used for inference so we can assume all graph outputs are model outputs.
    """
    *_, output_node = gm.graph.nodes
    out_list = output_node.args[0]
    with gm.graph.inserting_before(output_node):
        for n in out_list:
            if not isinstance(
                n.meta["val"], torch.Tensor
            ) or not torch._prims_common.is_non_overlapping_and_dense_or_false(
                n.meta["val"]
            ):
                continue

            # add a node to enforce eager layout
            ft = n.meta["val"]
            new_node = gm.graph.call_function(
                prims.inductor_force_stride_order.default, (n, ft.stride())
            )

            # can not call
            # n.replace_all_uses_with(new_node)
            # since it will replace the usage of n in new_node itself.
            output_node.replace_input_with(n, new_node)

    gm.graph.lint()
    gm.recompile()

