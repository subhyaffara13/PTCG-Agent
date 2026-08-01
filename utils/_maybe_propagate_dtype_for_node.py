
def _maybe_propagate_dtype_for_node(
    node: Node,
    target_dtype: torch.dtype | type,
    node_name_to_match_result_with_qconfig: dict[str, _MatchResultWithQConfig],
) -> None:
    """
    Assigns `target_dtype` to `node`, setting `is_dynamic` to False. If `node`
    is a general tensor shape op, also call this function recursively on
    the first argument, to propagate the dtype to the caller.
    """
    node.meta["target_dtype_info"]["input_act_obs_or_fq_ctr"] = None
    node.meta["target_dtype_info"]["output_act_obs_or_fq_ctr"] = None
    # if this is a copy node, propagate to first arg
    (
        _root_node,
        _,
        _pattern,
        qhandler,
        _qconfig,
    ) = node_name_to_match_result_with_qconfig.get(
        node.name, (None, None, None, None, None)
    )
    # TODO: probably need to remove `is_general_tensor_value_op`
    if qhandler is not None and qhandler.is_general_tensor_value_op():
        prev_node = node.args[0]
        if isinstance(prev_node, Node):
            _maybe_propagate_dtype_for_node(
                prev_node, target_dtype, node_name_to_match_result_with_qconfig
            )

