
def get_chunking_meta(node: Node) -> ChunkingMeta | None:
    return node.meta.get("chunking")

