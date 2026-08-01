
def multilabel_margin_loss_forward(
    input: Tensor,
    target: Tensor,
    reduction: int,
) -> tuple[Tensor, Tensor]:
    orig_input_shape = input.shape
    orig_target_shape = target.shape
    input = torch.atleast_2d(input)
    target = torch.atleast_2d(target)
    dim = input.shape[1]
    torch._check(
        len(orig_input_shape) <= 2 and dim != 0,
        lambda: f"Expected non-empty vector or matrix with optional 0-dim batch size, but got: {orig_input_shape}",
    )
    torch._check(
        len(orig_target_shape) <= 2 and orig_target_shape == orig_input_shape,
        lambda: f"inconsistent target size: {orig_target_shape} for input of size: {orig_input_shape}",
    )
    # ignores labels after the first -1, detects when -1 is not present
    idx = torch.arange(dim, device=target.device)
    is_end = target == -1
    end_idx = torch.amin(torch.where(is_end, idx, dim), dim=-1, keepdim=True)
    # target indices
    target_mask = idx < end_idx
    # masks target to be able to use gather, which doesn't allow -1
    tidx0 = torch.where(target_mask, target, 0)
    u = torch.gather(input, dim=-1, index=tidx0)
    # is_target
    tidx1 = torch.where(target_mask, target, -1)
    is_target = torch.any(idx == tidx1.unsqueeze(dim=-1), dim=1)
    # loss
    z = 1.0 - u.T.unsqueeze(dim=-1) + input
    z = z.clamp_min(0)
    z = z / dim
    # masks loss
    z = torch.where(is_target, 0, z)
    # reduction
    if reduction == Reduction.MEAN.value:
        z = z.sum(dim=(0, -1)).mean()
    elif reduction == Reduction.SUM.value:
        z = z.sum()
    else:
        z = z.sum(dim=(0, -1))
    # result
    is_target = is_target.to(input.dtype).reshape(orig_target_shape)
    return z, is_target

