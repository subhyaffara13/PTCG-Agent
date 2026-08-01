
def copy_chunking_meta(dst_node: Node, src_node: Node | ChunkingMeta) -> bool:
    if isinstance(src_node, torch.fx.Node):
        src_meta = get_chunking_meta(src_node)
    else:
        assert isinstance(src_node, ChunkingMeta)
        src_meta = src_node
    assert src_meta
    return set_chunking_meta(dst_node, src_meta)

