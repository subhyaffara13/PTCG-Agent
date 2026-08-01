
def build_2d_sinusoidal_position_embedding(
    height: int,
    width: int,
    embed_dim: int = 256,
    temperature: float = 10000.0,
    cls_token: bool = False,
    device: torch.device | None = None,
    dtype: torch.dtype = torch.float32,
) -> torch.Tensor:
    """2D sinusoidal position embeddings for an image patch grid.

    Each (h, w) position gets an ``embed_dim``-dimensional vector laid out as
    ``[sin_h | cos_h | sin_w | cos_w]``, with row-major (H-outer) patch ordering.

    Args:
        height: Grid height in patches.
        width: Grid width in patches.
        embed_dim: Total embedding dimension; must be divisible by 4.
        temperature: Base for the frequency decay.
        cls_token: If `True`, prepend a zero row for a CLS token.
        device: Target device; defaults to CPU.
        dtype: Output dtype; frequency arithmetic uses float64 internally.

    Returns:
        Tensor of shape ``(height * width [+1], embed_dim)``.
    """
    if embed_dim % 4 != 0:
        raise ValueError(f"`embed_dim` must be divisible by 4, got {embed_dim}")

    pos_dim = embed_dim // 4
    omega = torch.arange(pos_dim, dtype=torch.float64, device=device) / pos_dim
    omega = 1.0 / temperature**omega  # (D/4,)

    grid_h = torch.arange(height, dtype=torch.float64, device=device)
    grid_w = torch.arange(width, dtype=torch.float64, device=device)
    grid_h, grid_w = torch.meshgrid(grid_h, grid_w, indexing="ij")  # (H, W) each

    emb_h = grid_h.flatten().outer(omega)  # (H*W, D/4)
    emb_w = grid_w.flatten().outer(omega)  # (H*W, D/4)

    pos_embed = torch.cat([emb_h.sin(), emb_h.cos(), emb_w.sin(), emb_w.cos()], dim=1)

    if cls_token:
        pos_embed = torch.cat([torch.zeros(1, embed_dim, dtype=torch.float64, device=device), pos_embed], dim=0)

    return pos_embed.to(dtype)


def build_2d_sinusoidal_position_embedding(
    height: int,
    width: int,
    embed_dim: int = 256,
    temperature: float = 10000.0,
    cls_token: bool = False,
    device: torch.device | None = None,
    dtype: torch.dtype = torch.float32,
) -> torch.Tensor:
    """2D sinusoidal position embeddings for an image patch grid.

    Each (h, w) position gets an ``embed_dim``-dimensional vector laid out as
    ``[sin_h | cos_h | sin_w | cos_w]``, with row-major (H-outer) patch ordering.

    Args:
        height: Grid height in patches.
        width: Grid width in patches.
        embed_dim: Total embedding dimension; must be divisible by 4.
        temperature: Base for the frequency decay.
        cls_token: If `True`, prepend a zero row for a CLS token.
        device: Target device; defaults to CPU.
        dtype: Output dtype; frequency arithmetic uses float64 internally.

    Returns:
        Tensor of shape ``(height * width [+1], embed_dim)``.
    """
    if embed_dim % 4 != 0:
        raise ValueError(f"`embed_dim` must be divisible by 4, got {embed_dim}")

    pos_dim = embed_dim // 4
    omega = torch.arange(pos_dim, dtype=torch.float64, device=device) / pos_dim
    omega = 1.0 / temperature**omega  # (D/4,)

    grid_h = torch.arange(height, dtype=torch.float64, device=device)
    grid_w = torch.arange(width, dtype=torch.float64, device=device)
    grid_h, grid_w = torch.meshgrid(grid_h, grid_w, indexing="ij")  # (H, W) each

    emb_h = grid_h.flatten().outer(omega)  # (H*W, D/4)
    emb_w = grid_w.flatten().outer(omega)  # (H*W, D/4)

    pos_embed = torch.cat([emb_h.sin(), emb_h.cos(), emb_w.sin(), emb_w.cos()], dim=1)

    if cls_token:
        pos_embed = torch.cat([torch.zeros(1, embed_dim, dtype=torch.float64, device=device), pos_embed], dim=0)

    return pos_embed.to(dtype)


def build_2d_sinusoidal_position_embedding(
    height: int,
    width: int,
    embed_dim: int = 256,
    temperature: float = 10000.0,
    cls_token: bool = False,
    device: torch.device | None = None,
    dtype: torch.dtype = torch.float32,
) -> torch.Tensor:
    """2D sinusoidal position embeddings for an image patch grid.

    Each (h, w) position gets an ``embed_dim``-dimensional vector laid out as
    ``[sin_h | cos_h | sin_w | cos_w]``, with row-major (H-outer) patch ordering.

    Args:
        height: Grid height in patches.
        width: Grid width in patches.
        embed_dim: Total embedding dimension; must be divisible by 4.
        temperature: Base for the frequency decay.
        cls_token: If `True`, prepend a zero row for a CLS token.
        device: Target device; defaults to CPU.
        dtype: Output dtype; frequency arithmetic uses float64 internally.

    Returns:
        Tensor of shape ``(height * width [+1], embed_dim)``.
    """
    if embed_dim % 4 != 0:
        raise ValueError(f"`embed_dim` must be divisible by 4, got {embed_dim}")

    pos_dim = embed_dim // 4
    omega = torch.arange(pos_dim, dtype=torch.float64, device=device) / pos_dim
    omega = 1.0 / temperature**omega  # (D/4,)

    grid_h = torch.arange(height, dtype=torch.float64, device=device)
    grid_w = torch.arange(width, dtype=torch.float64, device=device)
    grid_h, grid_w = torch.meshgrid(grid_h, grid_w, indexing="ij")  # (H, W) each

    emb_h = grid_h.flatten().outer(omega)  # (H*W, D/4)
    emb_w = grid_w.flatten().outer(omega)  # (H*W, D/4)

    pos_embed = torch.cat([emb_h.sin(), emb_h.cos(), emb_w.sin(), emb_w.cos()], dim=1)

    if cls_token:
        pos_embed = torch.cat([torch.zeros(1, embed_dim, dtype=torch.float64, device=device), pos_embed], dim=0)

    return pos_embed.to(dtype)


def build_2d_sinusoidal_position_embedding(
    height: int,
    width: int,
    embed_dim: int = 256,
    temperature: float = 10000.0,
    cls_token: bool = False,
    device: torch.device | None = None,
    dtype: torch.dtype = torch.float32,
) -> torch.Tensor:
    """2D sinusoidal position embeddings for an image patch grid.

    Each (h, w) position gets an ``embed_dim``-dimensional vector laid out as
    ``[sin_h | cos_h | sin_w | cos_w]``, with row-major (H-outer) patch ordering.

    Args:
        height: Grid height in patches.
        width: Grid width in patches.
        embed_dim: Total embedding dimension; must be divisible by 4.
        temperature: Base for the frequency decay.
        cls_token: If `True`, prepend a zero row for a CLS token.
        device: Target device; defaults to CPU.
        dtype: Output dtype; frequency arithmetic uses float64 internally.

    Returns:
        Tensor of shape ``(height * width [+1], embed_dim)``.
    """
    if embed_dim % 4 != 0:
        raise ValueError(f"`embed_dim` must be divisible by 4, got {embed_dim}")

    pos_dim = embed_dim // 4
    omega = torch.arange(pos_dim, dtype=torch.float64, device=device) / pos_dim
    omega = 1.0 / temperature**omega  # (D/4,)

    grid_h = torch.arange(height, dtype=torch.float64, device=device)
    grid_w = torch.arange(width, dtype=torch.float64, device=device)
    grid_h, grid_w = torch.meshgrid(grid_h, grid_w, indexing="ij")  # (H, W) each

    emb_h = grid_h.flatten().outer(omega)  # (H*W, D/4)
    emb_w = grid_w.flatten().outer(omega)  # (H*W, D/4)

    pos_embed = torch.cat([emb_h.sin(), emb_h.cos(), emb_w.sin(), emb_w.cos()], dim=1)

    if cls_token:
        pos_embed = torch.cat([torch.zeros(1, embed_dim, dtype=torch.float64, device=device), pos_embed], dim=0)

    return pos_embed.to(dtype)


def build_2d_sinusoidal_position_embedding(
    height: int,
    width: int,
    embed_dim: int = 256,
    temperature: float = 10000.0,
    cls_token: bool = False,
    device: torch.device | None = None,
    dtype: torch.dtype = torch.float32,
) -> torch.Tensor:
    """2D sinusoidal position embeddings for an image patch grid.

    Each (h, w) position gets an ``embed_dim``-dimensional vector laid out as
    ``[sin_h | cos_h | sin_w | cos_w]``, with row-major (H-outer) patch ordering.

    Args:
        height: Grid height in patches.
        width: Grid width in patches.
        embed_dim: Total embedding dimension; must be divisible by 4.
        temperature: Base for the frequency decay.
        cls_token: If `True`, prepend a zero row for a CLS token.
        device: Target device; defaults to CPU.
        dtype: Output dtype; frequency arithmetic uses float64 internally.

    Returns:
        Tensor of shape ``(height * width [+1], embed_dim)``.
    """
    if embed_dim % 4 != 0:
        raise ValueError(f"`embed_dim` must be divisible by 4, got {embed_dim}")

    pos_dim = embed_dim // 4
    omega = torch.arange(pos_dim, dtype=torch.float64, device=device) / pos_dim
    omega = 1.0 / temperature**omega  # (D/4,)

    grid_h = torch.arange(height, dtype=torch.float64, device=device)
    grid_w = torch.arange(width, dtype=torch.float64, device=device)
    grid_h, grid_w = torch.meshgrid(grid_h, grid_w, indexing="ij")  # (H, W) each

    emb_h = grid_h.flatten().outer(omega)  # (H*W, D/4)
    emb_w = grid_w.flatten().outer(omega)  # (H*W, D/4)

    pos_embed = torch.cat([emb_h.sin(), emb_h.cos(), emb_w.sin(), emb_w.cos()], dim=1)

    if cls_token:
        pos_embed = torch.cat([torch.zeros(1, embed_dim, dtype=torch.float64, device=device), pos_embed], dim=0)

    return pos_embed.to(dtype)


def build_2d_sinusoidal_position_embedding(
    height: int,
    width: int,
    embed_dim: int = 256,
    temperature: float = 10000.0,
    cls_token: bool = False,
    device: torch.device | None = None,
    dtype: torch.dtype = torch.float32,
) -> torch.Tensor:
    """2D sinusoidal position embeddings for an image patch grid.

    Each (h, w) position gets an ``embed_dim``-dimensional vector laid out as
    ``[sin_h | cos_h | sin_w | cos_w]``, with row-major (H-outer) patch ordering.

    Args:
        height: Grid height in patches.
        width: Grid width in patches.
        embed_dim: Total embedding dimension; must be divisible by 4.
        temperature: Base for the frequency decay.
        cls_token: If `True`, prepend a zero row for a CLS token.
        device: Target device; defaults to CPU.
        dtype: Output dtype; frequency arithmetic uses float64 internally.

    Returns:
        Tensor of shape ``(height * width [+1], embed_dim)``.
    """
    if embed_dim % 4 != 0:
        raise ValueError(f"`embed_dim` must be divisible by 4, got {embed_dim}")

    pos_dim = embed_dim // 4
    omega = torch.arange(pos_dim, dtype=torch.float64, device=device) / pos_dim
    omega = 1.0 / temperature**omega  # (D/4,)

    grid_h = torch.arange(height, dtype=torch.float64, device=device)
    grid_w = torch.arange(width, dtype=torch.float64, device=device)
    grid_h, grid_w = torch.meshgrid(grid_h, grid_w, indexing="ij")  # (H, W) each

    emb_h = grid_h.flatten().outer(omega)  # (H*W, D/4)
    emb_w = grid_w.flatten().outer(omega)  # (H*W, D/4)

    pos_embed = torch.cat([emb_h.sin(), emb_h.cos(), emb_w.sin(), emb_w.cos()], dim=1)

    if cls_token:
        pos_embed = torch.cat([torch.zeros(1, embed_dim, dtype=torch.float64, device=device), pos_embed], dim=0)

    return pos_embed.to(dtype)


def build_2d_sinusoidal_position_embedding(
    height: int,
    width: int,
    embed_dim: int = 256,
    temperature: float = 10000.0,
    cls_token: bool = False,
    device: torch.device | None = None,
    dtype: torch.dtype = torch.float32,
) -> torch.Tensor:
    """2D sinusoidal position embeddings for an image patch grid.

    Each (h, w) position gets an ``embed_dim``-dimensional vector laid out as
    ``[sin_h | cos_h | sin_w | cos_w]``, with row-major (H-outer) patch ordering.

    Args:
        height: Grid height in patches.
        width: Grid width in patches.
        embed_dim: Total embedding dimension; must be divisible by 4.
        temperature: Base for the frequency decay.
        cls_token: If `True`, prepend a zero row for a CLS token.
        device: Target device; defaults to CPU.
        dtype: Output dtype; frequency arithmetic uses float64 internally.

    Returns:
        Tensor of shape ``(height * width [+1], embed_dim)``.
    """
    if embed_dim % 4 != 0:
        raise ValueError(f"`embed_dim` must be divisible by 4, got {embed_dim}")

    pos_dim = embed_dim // 4
    omega = torch.arange(pos_dim, dtype=torch.float64, device=device) / pos_dim
    omega = 1.0 / temperature**omega  # (D/4,)

    grid_h = torch.arange(height, dtype=torch.float64, device=device)
    grid_w = torch.arange(width, dtype=torch.float64, device=device)
    grid_h, grid_w = torch.meshgrid(grid_h, grid_w, indexing="ij")  # (H, W) each

    emb_h = grid_h.flatten().outer(omega)  # (H*W, D/4)
    emb_w = grid_w.flatten().outer(omega)  # (H*W, D/4)

    pos_embed = torch.cat([emb_h.sin(), emb_h.cos(), emb_w.sin(), emb_w.cos()], dim=1)

    if cls_token:
        pos_embed = torch.cat([torch.zeros(1, embed_dim, dtype=torch.float64, device=device), pos_embed], dim=0)

    return pos_embed.to(dtype)


def build_2d_sinusoidal_position_embedding(
    height: int,
    width: int,
    embed_dim: int = 256,
    temperature: float = 10000.0,
    cls_token: bool = False,
    device: torch.device | None = None,
    dtype: torch.dtype = torch.float32,
) -> torch.Tensor:
    """2D sinusoidal position embeddings for an image patch grid.

    Each (h, w) position gets an ``embed_dim``-dimensional vector laid out as
    ``[sin_h | cos_h | sin_w | cos_w]``, with row-major (H-outer) patch ordering.

    Args:
        height: Grid height in patches.
        width: Grid width in patches.
        embed_dim: Total embedding dimension; must be divisible by 4.
        temperature: Base for the frequency decay.
        cls_token: If `True`, prepend a zero row for a CLS token.
        device: Target device; defaults to CPU.
        dtype: Output dtype; frequency arithmetic uses float64 internally.

    Returns:
        Tensor of shape ``(height * width [+1], embed_dim)``.
    """
    if embed_dim % 4 != 0:
        raise ValueError(f"`embed_dim` must be divisible by 4, got {embed_dim}")

    pos_dim = embed_dim // 4
    omega = torch.arange(pos_dim, dtype=torch.float64, device=device) / pos_dim
    omega = 1.0 / temperature**omega  # (D/4,)

    grid_h = torch.arange(height, dtype=torch.float64, device=device)
    grid_w = torch.arange(width, dtype=torch.float64, device=device)
    grid_h, grid_w = torch.meshgrid(grid_h, grid_w, indexing="ij")  # (H, W) each

    emb_h = grid_h.flatten().outer(omega)  # (H*W, D/4)
    emb_w = grid_w.flatten().outer(omega)  # (H*W, D/4)

    pos_embed = torch.cat([emb_h.sin(), emb_h.cos(), emb_w.sin(), emb_w.cos()], dim=1)

    if cls_token:
        pos_embed = torch.cat([torch.zeros(1, embed_dim, dtype=torch.float64, device=device), pos_embed], dim=0)

    return pos_embed.to(dtype)


def build_2d_sinusoidal_position_embedding(
    height: int,
    width: int,
    embed_dim: int = 256,
    temperature: float = 10000.0,
    cls_token: bool = False,
    device: torch.device | None = None,
    dtype: torch.dtype = torch.float32,
) -> torch.Tensor:
    """2D sinusoidal position embeddings for an image patch grid.

    Each (h, w) position gets an ``embed_dim``-dimensional vector laid out as
    ``[sin_h | cos_h | sin_w | cos_w]``, with row-major (H-outer) patch ordering.

    Args:
        height: Grid height in patches.
        width: Grid width in patches.
        embed_dim: Total embedding dimension; must be divisible by 4.
        temperature: Base for the frequency decay.
        cls_token: If `True`, prepend a zero row for a CLS token.
        device: Target device; defaults to CPU.
        dtype: Output dtype; frequency arithmetic uses float64 internally.

    Returns:
        Tensor of shape ``(height * width [+1], embed_dim)``.
    """
    if embed_dim % 4 != 0:
        raise ValueError(f"`embed_dim` must be divisible by 4, got {embed_dim}")

    pos_dim = embed_dim // 4
    omega = torch.arange(pos_dim, dtype=torch.float64, device=device) / pos_dim
    omega = 1.0 / temperature**omega  # (D/4,)

    grid_h = torch.arange(height, dtype=torch.float64, device=device)
    grid_w = torch.arange(width, dtype=torch.float64, device=device)
    grid_h, grid_w = torch.meshgrid(grid_h, grid_w, indexing="ij")  # (H, W) each

    emb_h = grid_h.flatten().outer(omega)  # (H*W, D/4)
    emb_w = grid_w.flatten().outer(omega)  # (H*W, D/4)

    pos_embed = torch.cat([emb_h.sin(), emb_h.cos(), emb_w.sin(), emb_w.cos()], dim=1)

    if cls_token:
        pos_embed = torch.cat([torch.zeros(1, embed_dim, dtype=torch.float64, device=device), pos_embed], dim=0)

    return pos_embed.to(dtype)

