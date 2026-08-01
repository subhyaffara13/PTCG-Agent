
def propagate_addmm(addmm_node: Node) -> _HandlerRetType:
    bias_node, input_node, weight_node = addmm_node.args

    def propagate_addmm_fwd() -> PropagateStatus:
        assert isinstance(bias_node, Node)
        assert isinstance(input_node, Node)
        assert isinstance(weight_node, Node)
        if not has_any_chunking_meta(bias_node, input_node, weight_node):
            return PropagateStatus.SUCCEED_NO_CHANGE

        # only input is chunked by dim 0
        if (
            has_nop_chunking_meta(bias_node)
            and has_nop_chunking_meta(weight_node)
            and is_chunked_by_dim(input_node, 0)
        ):
            # set a nop chunking metadata on bias_node & weight_node
            # to indicate that they should be a part of the chunking
            # subgraph. (i.e. we pass in them as placeholder node)
            return _bool_to_status(
                copy_chunking_meta(addmm_node, input_node)
                | set_chunking_meta(bias_node)
                | set_chunking_meta(weight_node)
            )
        return PropagateStatus.FAIL

    def propagate_addmm_bwd() -> PropagateStatus:
        assert isinstance(bias_node, Node)
        assert isinstance(input_node, Node)
        assert isinstance(weight_node, Node)

        if not (meta := get_chunking_meta(addmm_node)):
            return PropagateStatus.SUCCEED_NO_CHANGE

        if meta.chunked_by_dim(0):
            # if the output is chunked by the batch dimension, then
            # bias and input should as well
            changed = set_chunking_meta(input_node, meta) | set_chunking_meta(
                weight_node
            )

            # We should chunk the bias only if it's not broadcasted
            bias_node_ft = get_fake_tensor_from_node_arg(bias_node)
            input_node_ft = get_fake_tensor_from_node_arg(input_node)
            assert bias_node_ft is not None
            assert input_node_ft is not None
            if bias_node_ft.ndim < input_node_ft.ndim:
                changed |= set_chunking_meta(bias_node)
            else:
                changed |= set_chunking_meta(bias_node, meta)
            return _bool_to_status(changed)

        return PropagateStatus.FAIL

    return propagate_addmm_fwd(), propagate_addmm_bwd()

