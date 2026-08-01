
def compute_embeddings(inv_freq: torch.Tensor, embed_height: int, embed_width: int, hidden_size: int) -> torch.Tensor:
    i_indices = torch.ones(embed_height, embed_width, dtype=inv_freq.dtype, device=inv_freq.device)
    j_indices = torch.ones(embed_height, embed_width, dtype=inv_freq.dtype, device=inv_freq.device)
    i_indices = i_indices.cumsum(0).unsqueeze(-1)
    j_indices = j_indices.cumsum(1).unsqueeze(-1)

    emb = torch.zeros(1, embed_height, embed_width, hidden_size // 2, dtype=inv_freq.dtype, device=inv_freq.device)
    emb[:, :, :, 0::2] = i_indices * inv_freq
    emb[:, :, :, 1::2] = j_indices * inv_freq

    return emb

