import math


def encode_sinusoidal_position_embedding(
    pos_tensor: torch.Tensor,
    num_pos_feats: int = 128,
    temperature: int = 10000,
) -> torch.Tensor:
    """Sinusoidal position embeddings from normalized anchor coordinates.

    Each coordinate in `pos_tensor` is independently encoded with ``num_pos_feats``
    interleaved sin/cos components; per-coordinate embeddings are concatenated.
    Handles 2-D ``(x, y)`` and N-D ``(x, y, w, h)`` inputs. For 2-D+ inputs the
    x and y embeddings are swapped to follow the DETR ``[pos_y, pos_x, ...]`` convention.

    Args:
        pos_tensor: Normalized coordinates in ``[0, 1]``, shape ``(..., n_coords)``.
        num_pos_feats: Embedding dimension per coordinate.
        temperature: Base for the frequency decay.

    Returns:
        Tensor of shape ``(..., n_coords * num_pos_feats)``, same dtype as input.
    """
    scale = 2 * math.pi
    dim_t = torch.arange(num_pos_feats, dtype=torch.float32, device=pos_tensor.device)
    dim_t = temperature ** (2 * torch.div(dim_t, 2, rounding_mode="floor") / num_pos_feats)

    coords = pos_tensor.unbind(-1)  # list of (...,) tensors
    embeddings = [coord[..., None] * scale / dim_t for coord in coords]  # each (..., num_pos_feats)
    embeddings = [
        torch.stack((e[..., 0::2].sin(), e[..., 1::2].cos()), dim=-1).flatten(-2) for e in embeddings
    ]  # each (..., num_pos_feats)

    if len(embeddings) >= 2:
        embeddings[0], embeddings[1] = embeddings[1], embeddings[0]

    return torch.cat(embeddings, dim=-1).to(pos_tensor.dtype)


def encode_sinusoidal_position_embedding(
    pos_tensor: torch.Tensor,
    num_pos_feats: int = 128,
    temperature: int = 10000,
) -> torch.Tensor:
    """Sinusoidal position embeddings from normalized anchor coordinates.

    Each coordinate in `pos_tensor` is independently encoded with ``num_pos_feats``
    interleaved sin/cos components; per-coordinate embeddings are concatenated.
    Handles 2-D ``(x, y)`` and N-D ``(x, y, w, h)`` inputs. For 2-D+ inputs the
    x and y embeddings are swapped to follow the DETR ``[pos_y, pos_x, ...]`` convention.

    Args:
        pos_tensor: Normalized coordinates in ``[0, 1]``, shape ``(..., n_coords)``.
        num_pos_feats: Embedding dimension per coordinate.
        temperature: Base for the frequency decay.

    Returns:
        Tensor of shape ``(..., n_coords * num_pos_feats)``, same dtype as input.
    """
    scale = 2 * math.pi
    dim_t = torch.arange(num_pos_feats, dtype=torch.float32, device=pos_tensor.device)
    dim_t = temperature ** (2 * torch.div(dim_t, 2, rounding_mode="floor") / num_pos_feats)

    coords = pos_tensor.unbind(-1)  # list of (...,) tensors
    embeddings = [coord[..., None] * scale / dim_t for coord in coords]  # each (..., num_pos_feats)
    embeddings = [
        torch.stack((e[..., 0::2].sin(), e[..., 1::2].cos()), dim=-1).flatten(-2) for e in embeddings
    ]  # each (..., num_pos_feats)

    if len(embeddings) >= 2:
        embeddings[0], embeddings[1] = embeddings[1], embeddings[0]

    return torch.cat(embeddings, dim=-1).to(pos_tensor.dtype)


def encode_sinusoidal_position_embedding(
    pos_tensor: torch.Tensor,
    num_pos_feats: int = 128,
    temperature: int = 10000,
) -> torch.Tensor:
    """Sinusoidal position embeddings from normalized anchor coordinates.

    Each coordinate in `pos_tensor` is independently encoded with ``num_pos_feats``
    interleaved sin/cos components; per-coordinate embeddings are concatenated.
    Handles 2-D ``(x, y)`` and N-D ``(x, y, w, h)`` inputs. For 2-D+ inputs the
    x and y embeddings are swapped to follow the DETR ``[pos_y, pos_x, ...]`` convention.

    Args:
        pos_tensor: Normalized coordinates in ``[0, 1]``, shape ``(..., n_coords)``.
        num_pos_feats: Embedding dimension per coordinate.
        temperature: Base for the frequency decay.

    Returns:
        Tensor of shape ``(..., n_coords * num_pos_feats)``, same dtype as input.
    """
    scale = 2 * math.pi
    dim_t = torch.arange(num_pos_feats, dtype=torch.float32, device=pos_tensor.device)
    dim_t = temperature ** (2 * torch.div(dim_t, 2, rounding_mode="floor") / num_pos_feats)

    coords = pos_tensor.unbind(-1)  # list of (...,) tensors
    embeddings = [coord[..., None] * scale / dim_t for coord in coords]  # each (..., num_pos_feats)
    embeddings = [
        torch.stack((e[..., 0::2].sin(), e[..., 1::2].cos()), dim=-1).flatten(-2) for e in embeddings
    ]  # each (..., num_pos_feats)

    if len(embeddings) >= 2:
        embeddings[0], embeddings[1] = embeddings[1], embeddings[0]

    return torch.cat(embeddings, dim=-1).to(pos_tensor.dtype)


def encode_sinusoidal_position_embedding(
    pos_tensor: torch.Tensor,
    num_pos_feats: int = 128,
    temperature: int = 10000,
) -> torch.Tensor:
    """Sinusoidal position embeddings from normalized anchor coordinates.

    Each coordinate in `pos_tensor` is independently encoded with ``num_pos_feats``
    interleaved sin/cos components; per-coordinate embeddings are concatenated.
    Handles 2-D ``(x, y)`` and N-D ``(x, y, w, h)`` inputs. For 2-D+ inputs the
    x and y embeddings are swapped to follow the DETR ``[pos_y, pos_x, ...]`` convention.

    Args:
        pos_tensor: Normalized coordinates in ``[0, 1]``, shape ``(..., n_coords)``.
        num_pos_feats: Embedding dimension per coordinate.
        temperature: Base for the frequency decay.

    Returns:
        Tensor of shape ``(..., n_coords * num_pos_feats)``, same dtype as input.
    """
    scale = 2 * math.pi
    dim_t = torch.arange(num_pos_feats, dtype=torch.float32, device=pos_tensor.device)
    dim_t = temperature ** (2 * torch.div(dim_t, 2, rounding_mode="floor") / num_pos_feats)

    coords = pos_tensor.unbind(-1)  # list of (...,) tensors
    embeddings = [coord[..., None] * scale / dim_t for coord in coords]  # each (..., num_pos_feats)
    embeddings = [
        torch.stack((e[..., 0::2].sin(), e[..., 1::2].cos()), dim=-1).flatten(-2) for e in embeddings
    ]  # each (..., num_pos_feats)

    if len(embeddings) >= 2:
        embeddings[0], embeddings[1] = embeddings[1], embeddings[0]

    return torch.cat(embeddings, dim=-1).to(pos_tensor.dtype)


def encode_sinusoidal_position_embedding(
    pos_tensor: torch.Tensor,
    num_pos_feats: int = 128,
    temperature: int = 10000,
) -> torch.Tensor:
    """Sinusoidal position embeddings from normalized anchor coordinates.

    Each coordinate in `pos_tensor` is independently encoded with ``num_pos_feats``
    interleaved sin/cos components; per-coordinate embeddings are concatenated.
    Handles 2-D ``(x, y)`` and N-D ``(x, y, w, h)`` inputs. For 2-D+ inputs the
    x and y embeddings are swapped to follow the DETR ``[pos_y, pos_x, ...]`` convention.

    Args:
        pos_tensor: Normalized coordinates in ``[0, 1]``, shape ``(..., n_coords)``.
        num_pos_feats: Embedding dimension per coordinate.
        temperature: Base for the frequency decay.

    Returns:
        Tensor of shape ``(..., n_coords * num_pos_feats)``, same dtype as input.
    """
    scale = 2 * math.pi
    dim_t = torch.arange(num_pos_feats, dtype=torch.float32, device=pos_tensor.device)
    dim_t = temperature ** (2 * torch.div(dim_t, 2, rounding_mode="floor") / num_pos_feats)

    coords = pos_tensor.unbind(-1)  # list of (...,) tensors
    embeddings = [coord[..., None] * scale / dim_t for coord in coords]  # each (..., num_pos_feats)
    embeddings = [
        torch.stack((e[..., 0::2].sin(), e[..., 1::2].cos()), dim=-1).flatten(-2) for e in embeddings
    ]  # each (..., num_pos_feats)

    if len(embeddings) >= 2:
        embeddings[0], embeddings[1] = embeddings[1], embeddings[0]

    return torch.cat(embeddings, dim=-1).to(pos_tensor.dtype)


def encode_sinusoidal_position_embedding(
    pos_tensor: torch.Tensor,
    num_pos_feats: int = 128,
    temperature: int = 10000,
) -> torch.Tensor:
    """Sinusoidal position embeddings from normalized anchor coordinates.

    Each coordinate in `pos_tensor` is independently encoded with ``num_pos_feats``
    interleaved sin/cos components; per-coordinate embeddings are concatenated.
    Handles 2-D ``(x, y)`` and N-D ``(x, y, w, h)`` inputs. For 2-D+ inputs the
    x and y embeddings are swapped to follow the DETR ``[pos_y, pos_x, ...]`` convention.

    Args:
        pos_tensor: Normalized coordinates in ``[0, 1]``, shape ``(..., n_coords)``.
        num_pos_feats: Embedding dimension per coordinate.
        temperature: Base for the frequency decay.

    Returns:
        Tensor of shape ``(..., n_coords * num_pos_feats)``, same dtype as input.
    """
    scale = 2 * math.pi
    dim_t = torch.arange(num_pos_feats, dtype=torch.float32, device=pos_tensor.device)
    dim_t = temperature ** (2 * torch.div(dim_t, 2, rounding_mode="floor") / num_pos_feats)

    coords = pos_tensor.unbind(-1)  # list of (...,) tensors
    embeddings = [coord[..., None] * scale / dim_t for coord in coords]  # each (..., num_pos_feats)
    embeddings = [
        torch.stack((e[..., 0::2].sin(), e[..., 1::2].cos()), dim=-1).flatten(-2) for e in embeddings
    ]  # each (..., num_pos_feats)

    if len(embeddings) >= 2:
        embeddings[0], embeddings[1] = embeddings[1], embeddings[0]

    return torch.cat(embeddings, dim=-1).to(pos_tensor.dtype)


def encode_sinusoidal_position_embedding(
    pos_tensor: torch.Tensor,
    num_pos_feats: int = 128,
    temperature: int = 10000,
) -> torch.Tensor:
    """Sinusoidal position embeddings from normalized anchor coordinates.

    Each coordinate in `pos_tensor` is independently encoded with ``num_pos_feats``
    interleaved sin/cos components; per-coordinate embeddings are concatenated.
    Handles 2-D ``(x, y)`` and N-D ``(x, y, w, h)`` inputs. For 2-D+ inputs the
    x and y embeddings are swapped to follow the DETR ``[pos_y, pos_x, ...]`` convention.

    Args:
        pos_tensor: Normalized coordinates in ``[0, 1]``, shape ``(..., n_coords)``.
        num_pos_feats: Embedding dimension per coordinate.
        temperature: Base for the frequency decay.

    Returns:
        Tensor of shape ``(..., n_coords * num_pos_feats)``, same dtype as input.
    """
    scale = 2 * math.pi
    dim_t = torch.arange(num_pos_feats, dtype=torch.float32, device=pos_tensor.device)
    dim_t = temperature ** (2 * torch.div(dim_t, 2, rounding_mode="floor") / num_pos_feats)

    coords = pos_tensor.unbind(-1)  # list of (...,) tensors
    embeddings = [coord[..., None] * scale / dim_t for coord in coords]  # each (..., num_pos_feats)
    embeddings = [
        torch.stack((e[..., 0::2].sin(), e[..., 1::2].cos()), dim=-1).flatten(-2) for e in embeddings
    ]  # each (..., num_pos_feats)

    if len(embeddings) >= 2:
        embeddings[0], embeddings[1] = embeddings[1], embeddings[0]

    return torch.cat(embeddings, dim=-1).to(pos_tensor.dtype)

