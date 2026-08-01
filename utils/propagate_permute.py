
def propagate_permute(permute_node: Node) -> _HandlerRetType:
    input_node, order = permute_node.args[:2]

    def propagate_fwd() -> PropagateStatus:
        assert isinstance(input_node, Node)
        assert isinstance(order, (tuple, list))
        input_meta = get_chunking_meta(input_node)
        output_meta = get_chunking_meta(permute_node)
        if input_meta is None:
            return _bool_to_status(False)

        if input_meta.chunk_dim is None:
            return PropagateStatus.FAIL

        orig_chunk_dim = input_meta.chunk_dim
        # pyrefly: ignore [bad-argument-type, bad-assignment]
        reverse_lookup: dict[int, int] = {v: k for k, v in enumerate(order)}
        new_chunk_dim = reverse_lookup[orig_chunk_dim]

        # sanity check
        if output_meta is not None:
            assert output_meta.chunk_dim == new_chunk_dim
        return _bool_to_status(
            set_chunking_meta(permute_node, meta=input_meta, chunk_dim=new_chunk_dim)
        )

    def propagate_bwd() -> PropagateStatus:
        assert isinstance(input_node, Node)
        assert isinstance(order, (tuple, list))

        input_meta = get_chunking_meta(input_node)
        output_meta = get_chunking_meta(permute_node)
        if output_meta is None:
            return _bool_to_status(False)

        if output_meta.chunk_dim is None:
            return PropagateStatus.FAIL

        orig_chunk_dim = output_meta.chunk_dim

        new_chunk_dim = order[orig_chunk_dim]

        # sanity check
        if input_meta is not None:
            assert input_meta.chunk_dim == new_chunk_dim
        return _bool_to_status(
            set_chunking_meta(input_node, meta=output_meta, chunk_dim=new_chunk_dim)
        )

    return propagate_fwd(), propagate_bwd()

