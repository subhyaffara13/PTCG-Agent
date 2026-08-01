
def propagate_view(view_node: Node) -> _HandlerRetType:
    input_node = view_node.args[0]
    assert isinstance(input_node, Node)
    input_shape = list(get_fake_tensor_from_node_arg(input_node).shape)  # type: ignore[union-attr]
    output_shape = list(get_fake_tensor_from_node_arg(view_node).shape)  # type: ignore[union-attr]

    def fwd() -> PropagateStatus:
        assert isinstance(input_node, Node)
        input_meta = get_chunking_meta(input_node)
        if input_meta is None:
            return _bool_to_status(False)
        if input_meta.chunk_dim is None:
            return _bool_to_status(copy_chunking_meta(view_node, input_meta))
        new_dim = _find_chunk_dim_after_reshape(
            input_shape, output_shape, input_meta.chunk_dim
        )
        if new_dim is None:
            return PropagateStatus.FAIL
        return _bool_to_status(
            set_chunking_meta(view_node, meta=input_meta, chunk_dim=new_dim)
        )

    def bwd() -> PropagateStatus:
        assert isinstance(input_node, Node)
        output_meta = get_chunking_meta(view_node)
        if output_meta is None:
            return _bool_to_status(False)
        if output_meta.chunk_dim is None:
            return _bool_to_status(copy_chunking_meta(input_node, output_meta))
        new_dim = _find_chunk_dim_after_reshape(
            output_shape, input_shape, output_meta.chunk_dim
        )
        if new_dim is None:
            return PropagateStatus.FAIL
        return _bool_to_status(
            set_chunking_meta(input_node, meta=output_meta, chunk_dim=new_dim)
        )

    return fwd(), bwd()

