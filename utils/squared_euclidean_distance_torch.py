
def squared_euclidean_distance_torch(a: torch.Tensor, b: torch.Tensor) -> torch.Tensor:
    """
    Compute squared Euclidean distances between all pixels and clusters.

    Args:
        a: (N, 3) tensor of pixel RGB values
        b: (M, 3) tensor of cluster RGB values

    Returns:
        (N, M) tensor of squared distances
    """
    b = b.t()  # (3, M)
    a2 = torch.sum(a**2, dim=1)  # (N,)
    b2 = torch.sum(b**2, dim=0)  # (M,)
    ab = torch.matmul(a, b)  # (N, M)
    d = a2[:, None] - 2 * ab + b2[None, :]  # Squared Euclidean Distance: a^2 - 2ab + b^2
    return d  # (N, M) tensor of squared distances

