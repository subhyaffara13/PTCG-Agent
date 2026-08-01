
def rotate_queries_or_keys(x, pos):
    B, num_heads, N, D = x.size()

    # similar to inv_freq = 1.0 / (theta ** (torch.arange(0, dim, 2, dtype=torch.float) / dim))
    # they are computing this every time. instead HF style is to compute the inv_freq once and store it
    # -- compute angle for each position
    omega = torch.arange(D // 2, dtype=x.dtype, device=x.device)
    omega /= D / 2.0
    omega = 1.0 / 10000**omega  # (D/2,)
    freq = pos.unsqueeze(-1) * omega  # (..., N, D/2), outer product

    # -- build rotation matrix and apply
    emb_sin = freq.sin()  # (..., N, D/2)
    emb_cos = freq.cos()  # (..., N, D/2)

    emb_sin = emb_sin.repeat(1, 1, 1, 2)
    emb_cos = emb_cos.repeat(1, 1, 1, 2)

    # --
    y = x.unflatten(-1, (-1, 2))
    y1, y2 = y.unbind(dim=-1)

    y = torch.stack((-y2, y1), dim=-1)
    y = y.flatten(-2)
    return (x * emb_cos) + (y * emb_sin)

