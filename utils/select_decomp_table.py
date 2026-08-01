
def select_decomp_table() -> dict[Any, Callable[..., Any]]:
    """decomps can change based on config"""
    if config.fallback_random:
        return decompositions
    if config.fallback_embedding_bag_byte_unpack:
        # remove q_embedding_bag_byte_unpack_decomp from decompositions
        decompositions.pop(torch.ops.quantized.embedding_bag_byte_unpack.default, None)
        return decompositions
    result = fast_random_decomps()
    return result

