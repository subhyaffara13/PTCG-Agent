
def _block_diag_iterable(tensors: list[TensorLikeType]) -> TensorLikeType:
    """
    Reference implementation of torch.block_diag
    """
    tensors_2d = [
        tensor.view(1, -1) if tensor.dim() <= 1 else tensor for tensor in tensors
    ]

    ncols = builtins.sum(tensor.shape[1] for tensor in tensors_2d)
    device = tensors_2d[0].device

    result = []

    col_start = 0
    for i, tensor in enumerate(tensors_2d):
        torch._check(
            tensor.dim() == 2,
            lambda: "Input tensors must have 2 or fewer dimensions. "
            f"Input {i} has {tensor.dim()} dimensions",
        )
        torch._check(
            tensor.device == device,
            lambda: "Input tensors must all be on the same device. "
            f"Input 0 is on device {device} and input {i} is on device {tensor.device}.",
        )
        row, col = tensor.shape
        left = torch.zeros((row, col_start), device=device, dtype=tensor.dtype)
        right = torch.zeros(
            (row, ncols - col_start - col), device=device, dtype=tensor.dtype
        )
        result += [torch.cat((left, tensor, right), dim=1)]
        col_start += col

    return torch.cat(result, dim=0)

