
def propagate_unsqueeze(unsqueeze_node: Node) -> _HandlerRetType:
    input_node, unsqueeze_dim = unsqueeze_node.args[:2]
    assert isinstance(input_node, Node)
    assert isinstance(unsqueeze_dim, int)
    input_ndim = get_fake_tensor_from_node_arg(input_node).ndim  # type: ignore[union-attr]
    # Normalize negative dim: unsqueeze valid range is [-(ndim+1), ndim]
    normalized_dim = (
        unsqueeze_dim + input_ndim + 1 if unsqueeze_dim < 0 else unsqueeze_dim
    )

    def fwd() -> PropagateStatus:
        assert isinstance(input_node, Node)
        input_meta = get_chunking_meta(input_node)
        if input_meta is None:
            return _bool_to_status(False)
        if input_meta.chunk_dim is None:
            return _bool_to_status(copy_chunking_meta(unsqueeze_node, input_meta))

        # pyrefly: ignore[unsupported-operation]
        new_dim = input_meta.chunk_dim + (
            1 if input_meta.chunk_dim >= normalized_dim else 0
        )
        return _bool_to_status(
            set_chunking_meta(unsqueeze_node, meta=input_meta, chunk_dim=new_dim)
        )

    def bwd() -> PropagateStatus:
        assert isinstance(input_node, Node)
        output_meta = get_chunking_meta(unsqueeze_node)
        if output_meta is None:
            return _bool_to_status(False)
        if output_meta.chunk_dim is None:
            return _bool_to_status(copy_chunking_meta(input_node, output_meta))
        # pyrefly: ignore[unsupported-operation]
        new_dim = output_meta.chunk_dim - (
            1 if output_meta.chunk_dim > normalized_dim else 0
        )
        return _bool_to_status(
            set_chunking_meta(input_node, meta=output_meta, chunk_dim=new_dim)
        )

    return fwd(), bwd()

