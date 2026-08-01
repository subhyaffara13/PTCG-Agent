
def _apply_rotary_emb(
    x: torch.Tensor,
    cos: torch.Tensor,
    sin: torch.Tensor,
) -> torch.Tensor:
    first_half, second_half = torch.chunk(x, 2, dim=-1)
    first_ = first_half * cos - second_half * sin
    second_ = second_half * cos + first_half * sin
    return torch.cat((first_, second_), dim=-1)


def _apply_rotary_emb(
    x: torch.Tensor,
    cos: torch.Tensor,
    sin: torch.Tensor,
) -> torch.Tensor:
    first_half, second_half = torch.chunk(x, 2, dim=-1)
    first_ = first_half * cos - second_half * sin
    second_ = second_half * cos + first_half * sin
    return torch.cat((first_, second_), dim=-1)


def _apply_rotary_emb(
    x: torch.Tensor,
    cos: torch.Tensor,
    sin: torch.Tensor,
) -> torch.Tensor:
    # Interleaving layout instead of concatenated
    first_half, second_half = x[..., ::2], x[..., 1::2]
    first_ = first_half * cos - second_half * sin
    second_ = second_half * cos + first_half * sin
    return torch.stack((first_, second_), dim=-1).flatten(-2)


def _apply_rotary_emb(
    x: torch.Tensor,
    cos: torch.Tensor,
    sin: torch.Tensor,
) -> torch.Tensor:
    # Interleaving layout instead of concatenated
    first_half, second_half = x[..., ::2], x[..., 1::2]
    first_ = first_half * cos - second_half * sin
    second_ = second_half * cos + first_half * sin
    return torch.stack((first_, second_), dim=-1).flatten(-2)

