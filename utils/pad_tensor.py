
def pad_tensor(
    tensor: torch.Tensor, pad_dim: int, pad_size: IntLikeType
) -> torch.Tensor:
    # During tracing, always emit the pad op even when pad_size=0 so all
    # ranks produce identical FX graph structure (SPMD).
    # guard_or_false returns False for symbolic sizes, so the pad is always
    # emitted during tracing. In eager with concrete pad_size=0, it returns
    # True and we skip the no-op pad.
    if guard_or_false(pad_size == 0) and not _are_we_tracing():
        return tensor
    pad = [0, 0] * (tensor.ndim - pad_dim)
    pad[-1] = pad_size  # pyrefly: ignore[unsupported-operation]
    return torch.nn.functional.pad(tensor, pad)


def pad_tensor(weight, group_size, k_blocks):
    """Pad tensor rowi so that it can be is divisible by group_size.

    Args:
        weight (array): weight
        group_size (int): how many elements share one scale/zp
        k_blocks (int): the number of block

    Returns:
        weight: paded weight
    """
    if group_size == -1:
        return weight

    org_w_shape = weight.shape
    padded_rows = k_blocks * group_size
    pad_len = padded_rows - org_w_shape[0]

    if pad_len > 0:
        weight = np.pad(weight, ((0, pad_len), (0, 0)), "constant")

    return weight

