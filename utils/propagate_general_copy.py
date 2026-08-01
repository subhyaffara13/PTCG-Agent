
def propagate_general_copy(out_node: Node) -> bool:
    """
    A rule that holds for multiple ops: the scale_by of the output is
    set to the only scale_by of input nodes or None if no input has scale_by
    set.
    """
    args_node = get_args_of_node_type(out_node)
    args_meta = get_chunking_metas(args_node)
    out_meta = get_chunking_meta(out_node)

    scale_by = get_scale_by_from_metas(*args_meta)  # type: ignore[arg-type]
    assert out_meta is not None
    out_meta.scale_by = scale_by
    return True

