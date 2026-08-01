
def _combine_routed_output(
    out_padded: torch.Tensor,
    sorted_weights: torch.Tensor,
    sentinel_mask: torch.Tensor,
    perm: torch.Tensor,
    sorted_to_padded: torch.Tensor,
    num_tokens: int,
    num_top_k: int,
    hidden_dim: int,
    out_dtype: torch.dtype,
) -> torch.Tensor:
    """Unpad → weighted multiply → mask sentinels → restore order → top-k reduce."""
    out = _unpad_from_deepgemm_contiguous_layout(out_padded, sorted_to_padded)
    weighted = out * sorted_weights.to(out.dtype).unsqueeze(-1)
    # Sentinel rows past the valid expert blocks may carry NaN from allocator
    # reuse (`0 * NaN = NaN`); zero them so the top-k reduction stays finite.
    weighted.masked_fill_(sentinel_mask, 0.0)
    inv_perm = torch.empty_like(perm)
    inv_perm[perm] = torch.arange(perm.size(0), device=out.device)
    # Deterministic reshape+sum (index_add_ with duplicates is non-deterministic on CUDA).
    return weighted[inv_perm].view(num_tokens, num_top_k, hidden_dim).sum(dim=1).to(out_dtype)

