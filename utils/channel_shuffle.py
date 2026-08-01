
def channel_shuffle(input: TensorLikeType, groups: int) -> TensorLikeType:
    """
    Reference implementation of :func:`torch.nn.functional.channel_shuffle`.
    """
    from torch._meta_registrations import device_hint

    torch._check(
        input.dim() > 2,
        lambda: f"channel_shuffle expects input with > 2 dims, but got input with sizes {list(input.size())}",
    )
    c = input.shape[1]
    torch._check(
        groups > 0,
        lambda: f"Number of groups to divide channels in must be positive. Value of groups:{groups}",
    )
    torch._check(
        (c % groups) == 0,
        lambda: f"Number of channels must be divisible by groups. Got {c} channels and {groups} groups.",
    )
    n = input.shape[0]
    cg = c // groups
    dhw = input.shape[2:]

    if input.numel() == 0 or (
        device_hint(input) == "cuda" and (groups == 1 or groups == c)
    ):
        return input.view(input.shape)

    return (
        input.reshape(n, groups, cg, *dhw)
        .transpose(1, 2)
        .reshape(input.shape)
        .contiguous()
    )

