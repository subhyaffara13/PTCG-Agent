
def propagate_expand(expand_node: Node) -> _HandlerRetType:
    input_node = expand_node.args[0]
    assert isinstance(input_node, Node)

    input_ft = get_fake_tensor_from_node_arg(input_node)
    assert input_ft is not None
    output_ft = get_fake_tensor_from_node_arg(expand_node)
    assert output_ft is not None
    input_shape = list(input_ft.shape)
    output_shape = list(output_ft.shape)

    if input_ft.numel() == 1:
        # Scalar input: combined fwd/bwd rule
        output_meta = get_chunking_meta(expand_node)
        if output_meta is None:
            return _bool_to_status(False)
        return _bool_to_status(set_chunking_meta(input_node))

    # How many leading dims are added by expand
    dim_offset = len(output_shape) - len(input_shape)

    def is_expand_dim(out_dim: int) -> bool:
        """Check if out_dim is a broadcast dimension (newly added or size 1 in input)."""
        return out_dim < dim_offset or input_shape[out_dim - dim_offset] == 1

    def fwd() -> PropagateStatus:
        assert isinstance(input_node, Node)
        input_meta = get_chunking_meta(input_node)
        if input_meta is None:
            return _bool_to_status(False)
        # Fail if chunk_dim is an expand dimension (input size 1 broadcast to larger size)
        if input_meta.chunk_dim is not None and is_expand_dim(
            input_meta.chunk_dim + dim_offset
        ):
            return PropagateStatus.FAIL
        return _bool_to_status(copy_chunking_meta(expand_node, input_meta))

    def bwd() -> PropagateStatus:
        assert isinstance(input_node, Node)
        output_meta = get_chunking_meta(expand_node)
        if output_meta is None:
            return _bool_to_status(False)
        # Fail if chunk_dim is an expand dimension (input size 1 broadcast to larger size)
        if output_meta.chunk_dim is not None and is_expand_dim(output_meta.chunk_dim):
            return PropagateStatus.FAIL
        return _bool_to_status(copy_chunking_meta(input_node, output_meta))

    return fwd(), bwd()

