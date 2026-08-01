
def prune_conv2d_conv2d(conv2d_1: nn.Conv2d, conv2d_2: nn.Conv2d) -> None:
    prune_conv2d_activation_conv2d(conv2d_1, None, conv2d_2)

