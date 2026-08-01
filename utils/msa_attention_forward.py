
def msa_attention_forward(
    module: torch.nn.Module,
    query: torch.Tensor,
    key: torch.Tensor,
    value: torch.Tensor,
    attention_mask: torch.Tensor | None = None,
    dropout: float = 0.0,
    scaling: float | None = None,
    block_indices: torch.Tensor | None = None,
    **kwargs,
) -> tuple[torch.Tensor, None]:
    """
    TODO: this opens a door to per-layer attn implementation which is something we might want lalter on.
    """
    if scaling is None:
        scaling = query.shape[-1] ** -0.5

    # No block selection (the dense vision tower, or full-attention layers without an indexer) -> plain SDPA.
    if block_indices is None:
        return sdpa_attention_forward(
            module, query, key, value, attention_mask, dropout=dropout, scaling=scaling, **kwargs
        )

    # A sparse layer always runs the MSA kernel -- there is no SDPA fallback. Capability/config is
    # validated once per module (raises on unsupported hardware or config) and cached on the module.
    if not getattr(module, "_msa_validated", False):
        _validate_msa_init(module, query, dropout)
        module._msa_validated = True

    block_size = module.indexer.block_size
    cache_position = kwargs.get("cache_position")
    attn_output = _sparse_attention(module, query, key, value, scaling, block_indices, block_size, cache_position)
    return attn_output, None

