
def prune_conv2d_activation_pool_conv2d(
    c1: nn.Conv2d,
    activation: Callable[[Tensor], Tensor] | None,
    pool: nn.Module,
    c2: nn.Conv2d,
) -> None:
    prune_conv2d_activation_conv2d(c1, activation, c2)

