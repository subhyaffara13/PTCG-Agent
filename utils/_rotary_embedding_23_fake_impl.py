
def _rotary_embedding_23_fake_impl(
    x: torch.Tensor,
    cos_cache: torch.Tensor,
    sin_cache: torch.Tensor,
    position_ids: torch.Tensor | None = None,
    *,
    interleaved: bool = False,
    num_heads: int = 0,
    rotary_embedding_dim: int = 0,
) -> torch.Tensor:
    """Fake implementation for RotaryEmbedding-23 for torch.compile purposes."""
    return x.clone()

