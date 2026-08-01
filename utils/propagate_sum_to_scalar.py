
def propagate_sum_to_scalar(sum_node: Node) -> _HandlerRetType:
    input_node = sum_node.args[0]
    assert isinstance(input_node, Node)

    def fwd() -> PropagateStatus:
        input_meta = get_chunking_meta(input_node)  # pyrefly: ignore[bad-argument-type]
        if has_nop_chunking_meta(input_node):  # pyrefly: ignore[bad-argument-type]
            return _bool_to_status(False)

        assert input_meta is not None
        if input_meta.chunk_dim is not None:
            changed = update_chunking_meta(sum_node, need_sum=True, chunk_by=None)
            return _bool_to_status(changed)
        return PropagateStatus.FAIL

    def bwd() -> PropagateStatus:
        input_meta = get_chunking_meta(input_node)  # pyrefly: ignore[bad-argument-type]
        if has_nop_chunking_meta(sum_node):
            return _bool_to_status(False)

        # We won't know how the input is chunked if sum_node.meta.need_sum is True.
        # On the other hand, sum_node.meta.need_sum is True can only happen
        # by propagating from input_node. Doing sanity check here is fine
        # since the input_node.meta should have already been properly
        # setup.
        output_meta = get_chunking_meta(sum_node)
        if (
            output_meta is not None
            and output_meta.need_sum
            and input_meta is not None
            and input_meta.chunk_dim is not None
        ):
            return _bool_to_status(False)

        return PropagateStatus.FAIL

    return fwd(), bwd()

