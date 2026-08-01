
def do_pool(x: torch.Tensor, query_stride: int | None = None) -> torch.Tensor:
    if query_stride is None:
        return x
    # (B, H, W, C) -> (B, C, H, W)
    x = x.permute(0, 3, 1, 2)
    x = nn.functional.max_pool2d(x, kernel_size=query_stride, stride=query_stride, ceil_mode=False)
    # (B, C, H', W') -> (B, H', W', C)
    x = x.permute(0, 2, 3, 1)
    return x


def do_pool(x: torch.Tensor, query_stride: int | None = None) -> torch.Tensor:
    if query_stride is None:
        return x
    # (B, H, W, C) -> (B, C, H, W)
    x = x.permute(0, 3, 1, 2)
    x = nn.functional.max_pool2d(x, kernel_size=query_stride, stride=query_stride, ceil_mode=False)
    # (B, C, H', W') -> (B, H', W', C)
    x = x.permute(0, 2, 3, 1)
    return x

