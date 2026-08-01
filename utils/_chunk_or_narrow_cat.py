
def _chunk_or_narrow_cat(
    tensor: "torch.Tensor",
    num_chunks: int,
    narrow_dim: int,
    cat_dim: int = 0,
) -> "torch.Tensor":
    """
    Splits tensor along narrow_dim into num_chunks and concatenates along cat_dim.
    Uses torch.chunk in eager mode, but torch.narrow under tracing to be unbacked-symint safe.
    """
    if torch.distributed.is_available():
        from torch.distributed._functional_collectives import _are_we_tracing
        from torch.fx.experimental.symbolic_shapes import has_free_unbacked_symbols

        # TODO(pianpwk): remove the unbacked symbols check and fix AsyncTP pattern matching
        # for test_micro_pipeline_tp.py.
        if _are_we_tracing() and has_free_unbacked_symbols(tensor):
            chunk_size = tensor.size(narrow_dim) // num_chunks
            chunks = [
                torch.narrow(tensor, narrow_dim, i * chunk_size, chunk_size)
                for i in range(num_chunks)
            ]
            return torch.cat(chunks, dim=cat_dim)
    return torch.cat(torch.chunk(tensor, num_chunks, dim=narrow_dim), dim=cat_dim)

