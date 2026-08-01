
def rotate_pairwise(x):
    """
    pairwise rotation of the hidden dims of the input. Differerent from Llama Half-Tensor Rotation.

    This is an optimized version of the following more explicit implementation:
    ```python
    x_rotated = torch.zeros_like(x, dtype=x.dtype, device=x.device)
    x_rotated[..., ::2] = -x[..., 1::2]
    x_rotated[..., 1::2] = x[..., ::2]
    return x_rotated
    ```
    """
    x = x.view(*x.shape[:-1], -1, 2)
    x1, x2 = x.unbind(dim=-1)
    x = torch.stack((-x2, x1), dim=-1)
    return x.flatten(start_dim=-2)


def rotate_pairwise(x):
    """
    pairwise rotation of the hidden dims of the input. Differerent from Llama Half-Tensor Rotation.

    This is an optimized version of the following more explicit implementation:
    ```python
    x_rotated = torch.zeros_like(x, dtype=x.dtype, device=x.device)
    x_rotated[..., ::2] = -x[..., 1::2]
    x_rotated[..., 1::2] = x[..., ::2]
    return x_rotated
    ```
    """
    x = x.view(*x.shape[:-1], -1, 2)
    x1, x2 = x.unbind(dim=-1)
    x = torch.stack((-x2, x1), dim=-1)
    return x.flatten(start_dim=-2)


def rotate_pairwise(x):
    """
    pairwise rotation of the hidden dims of the input. Differerent from Llama Half-Tensor Rotation.

    This is an optimized version of the following more explicit implementation:
    ```python
    x_rotated = torch.zeros_like(x, dtype=x.dtype, device=x.device)
    x_rotated[..., ::2] = -x[..., 1::2]
    x_rotated[..., 1::2] = x[..., ::2]
    return x_rotated
    ```
    """
    x = x.view(*x.shape[:-1], -1, 2)
    x1, x2 = x.unbind(dim=-1)
    x = torch.stack((-x2, x1), dim=-1)
    return x.flatten(start_dim=-2)


def rotate_pairwise(x):
    """
    pairwise rotation of the hidden dims of the input. Differerent from Llama Half-Tensor Rotation.

    This is an optimized version of the following more explicit implementation:
    ```python
    x_rotated = torch.zeros_like(x, dtype=x.dtype, device=x.device)
    x_rotated[..., ::2] = -x[..., 1::2]
    x_rotated[..., 1::2] = x[..., ::2]
    return x_rotated
    ```
    """
    x = x.view(*x.shape[:-1], -1, 2)
    x1, x2 = x.unbind(dim=-1)
    x = torch.stack((-x2, x1), dim=-1)
    return x.flatten(start_dim=-2)


def rotate_pairwise(x):
    """
    pairwise rotation of the hidden dims of the input. Differerent from Llama Half-Tensor Rotation.

    This is an optimized version of the following more explicit implementation:
    ```python
    x_rotated = torch.zeros_like(x, dtype=x.dtype, device=x.device)
    x_rotated[..., ::2] = -x[..., 1::2]
    x_rotated[..., 1::2] = x[..., ::2]
    return x_rotated
    ```
    """
    x = x.view(*x.shape[:-1], -1, 2)
    x1, x2 = x.unbind(dim=-1)
    x = torch.stack((-x2, x1), dim=-1)
    return x.flatten(start_dim=-2)

